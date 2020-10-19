from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

from model.Cargo import Cargo
from model.User import User
from model.Types_reg import TypesReg
from model.Documents import Documents
from model.Department import Department
from admin.Views import UserView, HomeView, DocumentsView, CargoView, DepartmentView, TyperegView


def start_views(app, db):
    admin = Admin(app, name='Catálogo', base_template='admin/base.html',
                  template_mode='bootstrap3', index_view=HomeView())
    admin.add_view(CargoView(Cargo, db.session, "Cargos", category="Usuários"))
    admin.add_view(UserView(User, db.session, "Usuários", category="Usuários"))
    admin.add_view(DepartmentView(Department, db.session, "Setores", category="Usuários"))
    admin.add_view(TyperegView(TypesReg, db.session, "Tipos de Registro", category="Documentos"))
    admin.add_view(DocumentsView(Documents, db.session, "Documentos", category="Documentos"))

    admin.add_link(MenuLink(name='Logout', url='/logout'))
