from flask_login import LoginManager, login_user, logout_user
from flask import Flask, request, redirect, render_template, Response, json, abort
from config import app_config, app_active
from controller.User import UserController
from admin.Admin import start_views
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from controller.Documents import DocumentController
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

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Conten-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args, **kwargs):
            user = UserController()
            try:
                result = user.verify_auth_token(request.headers['access_token'])
                if result['status'] == 200:
                    return f(*args, **kwargs)
                else:
                    abort(result['status'], result['message'])
            except KeyError as e:
                abort(401, 'Você precisa enviar um token de acesso')
        return verify_token

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

    @app.route('/documents', methods=['POST'])
    def save_documents():
        document = DocumentController

        result = document.save_document(request.form)

        if result:
            message = "Inserido"
        else:
            message = "Não inserido"
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

    @app.route('/registro/')
    def registro():
        return render_template('registro.html')

    @app.route('/documents/', methods=['GET'])
    @app.route('/documents/<limit>', methods=['GET'])
    @auth_token_required
    def get_documents(limit=None):
        header = {
            'access_token': request.headers['access_token'],
            'token_type': 'jwt'
        }

        documents = DocumentController()
        response = documents.get_documents(limit=limit)

        return Response(json.dumps(response,
                                   ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/documents/<documents_id>', methods=['GET'])
    @auth_token_required
    def get_document(documents_id):
        header = {
            'access_token': request.headers['access_token'],
            'token_type': 'jwt'
        }

        documents = DocumentController()
        response = documents.get_documents_by_id(documents_id=documents_id)

        return Response(json.dumps(response,
                                   ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/user/<user_id>', methods=['GET'])
    @auth_token_required
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

"""
Boa prática é definir o nome do pacote do app FLASK, __name__ não é uma boa prática.
"""