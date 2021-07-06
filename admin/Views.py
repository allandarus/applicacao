from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect
from model.User import User
from model.Types_reg import TypesReg
from model.Documents import Documents
from config import app_config, app_active

config = app_config[app_active]


class HomeView(AdminIndexView):
    extra_css = [config.URL_MAIN + 'static/css/home.css',
                 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']

    @expose('/')
    def index(self):
        user_model = User()
        typesreg_model = TypesReg()
        documents_model = Documents()

        users = user_model.get_total_users()
        typesregs = typesreg_model.get_total_types()
        documents = documents_model.get_total_documents()

        last_documents = documents_model.get_last_documents()

        return self.render('home_admin.html', report={
            'users': 0 if not users else users[0],
            'typesreg': 0 if not typesregs else typesregs[0],
            'documents': 0 if not documents else documents[0]
        }, last_documents=last_documents)


class UserView(ModelView):
    column_labels = {'funcao': 'Função',
                     'setor': 'Setor',
                     'username': 'Usuário',
                     'email': 'E-mail',
                     'data_created': 'Data de criação',
                     'last_updated': 'Última atualização',
                     'active': 'Ativo',
                     'password': 'Senha'}

    column_descriptions = {
        'funcao': 'Função no sistema, controle de níveis de acesso',
        'setor': 'Setor onde o usuário está alocado',
        'username': 'Login do usuário',
        'email': 'Endereço de email para contato do usuário',
        'data_created': 'Data que o usuário é cadastrado no sistema,',
        'last_updated': 'Data mais recente em que as informações do usuário foram atualizadas',
        'active': 'Marque a opção se o usuário ainda está em atividades na Fundação',
        'password': 'Senha para acesso'
    }

    column_exclude_list = ['password', 'recovery_code']
    form_excluded_columns = ['last_update', 'recovery_code']

    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }

    can_set_page_size = True
    can_view_details = True
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email', 'funcao']
    column_editable_list = ['username', 'email', 'funcao', 'active']
    create_modal = True
    edit_modal = True
    can_export = True
    column_sortable_list = ['username']
    column_default_sort = ('username', True)
    column_details_exclude_list = ['recovery_password']
    column_export_exclude_list = ['password', 'recovery_password']
    export_types = ['json', 'yaml', 'csv', 'xls', 'df']

    def on_model_change(self, form, User, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password


class DocumentsView(ModelView):
    column_labels = {
        'num_reg': 'Nº de Registro',
        'objeto': 'Objeto',
        'origen': 'Origem',
        'date_created': 'Data de Criação',
        'criador': 'Solicitante',
        'creator': 'Criado por',
        'destiny': 'Destino'
    }

    column_descriptions = {
        'num_reg': 'Número gerado pelo sistema do arquivo',
        'objeto': 'Breve descrição do conteúdo do documento',
        'origen': 'Setor de origem do documento que foi gerado',
        'data_created': 'Data de Criação',
        'requester': 'Usuário solicitante',
        'creator': 'Usuário que registrou o documento no sistema',
        'destiny': 'Destino do documento',
    }

    can_set_page_size = True
    can_view_details = True
    column_searchable_list = ['num_reg', 'destiny', 'date_created']
    column_filters = ['origen', 'destiny', 'requester', 'creator']
    column_editable_list = ['objeto', 'origen', 'destiny', 'requester']
    create_modal = True
    edit_modal = True
    can_export = True
    column_sortable_list = ['date_created']
    column_default_sort = ('date_created', False)
    export_types = ['json', 'yaml', 'csv', 'xls', 'df']


class CargoView(ModelView):
    column_labels = {
        'name': 'Nome',
        'description': 'Descrição'
    }

    column_descriptions = {
        'name': 'Nome do grupo de usuário',
        'description': 'Permissões do grupo'
    }
    create_modal = True
    edit_modal = True


class DepartmentView(ModelView):
    column_labels = {
        'name': 'Nome do setor',
        'tipo': 'Tipo de Destino',
        'description': 'Descrição do setor'
    }

    column_descriptions = {
        'tipo': 'Escolha 1 para setores FESF, 2 para Externo privados e 3 para Externos governos',
        'description': 'Preencher no formato: "Diretoria-Nome completo do setor"'
    }

    column_editable_list = ['name', 'tipo', 'description']
    create_modal = True
    edit_modal = True


class TyperegView(ModelView):
    column_labels = {
        'name': 'Nome',
        'description': 'Descrição'
    }

    column_descriptions = {
        'description': 'Descricão do tipo de registro'
    }

    create_modal = True
    edit_modal = True
    can_view_details = True
