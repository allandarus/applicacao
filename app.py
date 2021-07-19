from flask.helpers import flash
from flask_login import LoginManager, login_user, logout_user
from flask import Flask, request, redirect, render_template, Response, json, jsonify, url_for, session, flash
from config import app_config, app_active
from controller.User import UserController
from admin.Admin import start_views
from flask_sqlalchemy import SQLAlchemy, functools
from sqlalchemy import func
from flask_wtf import FlaskForm
from functools import wraps
from controller.Documents import DocumentController
from model.Documents import Documents, get_count
from model.Department import Department
from controller.Department import DepartmentController
from wtforms_sqlalchemy.fields import QuerySelectField
from model.Types_reg import TypesReg
from datetime import datetime
from static.cadastro import FormCadastro, cont_reg
from flask_bootstrap import Bootstrap

config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
    db = SQLAlchemy(config.APP)
    start_views(app, db)
    Bootstrap(app)
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template('base.html')

    @app.route('/login/')
    def login():
        return render_template('login.html', data={'status': 200, 'msg': None, 'type': None})

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()

        email = request.form['email']
        password = request.form['password']

        result = user.login(email, password)

        if result:
            if result.role == 3:
                return render_template('login.html',
                                       data={'status': 401, 'msg': 'Seu usuário não tem permissão para acessar o admin',
                                             'type': 2})
            else:
                login_user(result)
                return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': 1})

    @app.route('/recupere-senha')
    def recovery_password():
        return 'Recuperação de Senha'

    @app.route('/recupere-senha', methods=['Post'])
    def send_recovery_password():
        user = UserController()

        result = user.recovery(request.form['email'])

        if result:
            return render_template('recovery.html', data={
                'status': 200, 'msg': 'E-mail de confirmação enviado com sucesso'})
        else:
            return render_template('recovery.hmtl', data={'status': 401, 'msg': 'Erro ao enviar e-mail de confirmação'})

    @app.route('/cadastro/', methods=['GET', 'POST'])
    def cadastro_salvar():
        """
        Função para salvar os dados do formulário no banco de dados.
        Caso envie dados, o sistesma guarda a data atual e o tipo de registro
        que há no formulário. Em seguida faz uma pesquisa na tabela 'Documents'
        no banco de dados. Próximo passo aciona a função 'get_count' que se
        encontra na model Documentos.py e soma mais 1 para ter a número atual
        incluindo o novo registro. Ao validadr o formulário, ele salva no banco
        os dados do formulários equivalentes ao campo. O campo 'num_reg', chama
        a função 'cont_reg', localizada em static/cadastro.py para transformar
        os dados obtidos e guardados em 'data_created' e 'n_rows' no formato
        string utilizado como númeração padrão: 00X/aaaa (ex: 001/2021)
        """
        form = FormCadastro()

        if request.method == 'POST':
            date_created = datetime.now()
            tipo = form.tipo_reg.data.name
            q = db.session.query(Documents).filter(Documents.type==tipo)
            n_rows = get_count(q) + 1

            if form.validate_on_submit():
                doc = Documents(num_reg = cont_reg(date_created, n_rows), 
                objeto = form.objeto.data, origen = form.origem.data,
                destiny = form.destino.data, 
                date_created = form.date_criacao.data,
                requester = form.solicitante.data, 
                creator = form.criador.data,
                type = form.tipo_reg.data)
                db.session.add(doc)
                db.session.commit()
                flash('Sucesso ao gravar')

                return render_template('base.html')

        return render_template('cadastro.html', form=form)

    @app.route('/destino/<get_destino>', methods=['GET'])
    def destino_opcoes(get_destino):
        destinos = Department.query.filter_by(tipo=get_destino).all()

        destinos_conj = []

        for destino in destinos:
            destinobj = {}
            destinobj['id'] = destino.id
            destinobj['name'] = destino.name
            destinobj['tipo'] = destino.tipo
            destinobj['description'] = destino.description
            destinos_conj.append(destinobj)

        return jsonify({'destinos': destinos_conj})

    @app.route('/documents', methods=['POST', 'GET'])
    def save_documents():
        document = DocumentController

        result = document.save_document(request.form)

        if result:
            message = 'Editado'
        else:
            message = "Não editado"
        return message

    @app.route('/documents', methods=['PUT'])
    def update_documents():
        document = DocumentController

        result = document.update_document(request.form)

        if result:
            message = 'Editado'
        else:
            message = "Não editado"
        return message

    @app.route('/documents/', methods=['GET'])
    @app.route('/documents/<limit>', methods=['GET'])
    def get_documents(limit=None):
        header = {}

        documents = DocumentController()
        response = documents.get_documents(limit=limit)

        return Response(json.dumps(response,
                                   ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/documents/<documents_id>', methods=['GET'])
    def get_document(doc_id):
        header = {}

        documents = DocumentController()
        response = documents.get_documents_by_id(documents_id=doc_id)

        return Response(json.dumps(response,
                                   ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/user/<user_id>', methods=['GET'])
    def get_user_profile(user_id):
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "jwt"
        }

        user = UserController()
        response = user.get_user_by_id(user_id=user_id)

        return Response(json.dumps(response,
                                   ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/login_api/', methods=['POST'])
    def login_api():
        header = {}
        user = UserController()

        email = request.json['email']
        password = request.json['password']

        result = user.login(email, password)
        code = 401
        response = {"message": "Usuário não autorizado", "result": []}

        if result:
            if result.active:
                result = {
                    'id': result.id,
                    'username': result.username,
                    'email': result.email,
                    'date_created': result.date_created,
                    'active': result.active
                }

                header = {
                    "access_token": user.generate_auth_token(result),
                    "token_type": "JWT"
                }
                code = 200
                response["message"] = "Login realizado com sucesso"
                response["result"] = result

        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), code, header

    @app.route('/logout')
    def logout_send():
        logout_user()
        return render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso',
                                                   'type': 3})

    @login_manager.user_loader
    def loader(user_id):
        user = UserController()
        return user.get_admin_login(user_id)

    return app
