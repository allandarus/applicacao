from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import func
from config import app_config, app_active
from model.Cargo import Cargo
from model.Department import Department
from passlib.hash import pbkdf2_sha256

config = app_config[app_active]

db = SQLAlchemy(config.APP)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(260), nullable=False)
	date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
	last_update = db.Column(db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=True)
	recovery_code = db.Column(db.String(200), nullable=True)
	department = db.Column(db.String(40), db.ForeignKey(Department.id), nullable=False)
	active = db.Column(db.Boolean(), default=1, nullable=True)
	cargo = db.Column(db.Integer, db.ForeignKey(Cargo.id), nullable=False)

	funcao = relationship(Cargo)
	setor = relationship(Department)

	def __repr__(self):
		return f'{self.username}'

	def get_user_by_email(self):
		try:
			res = db.session.query(User).filter(User.email == self.email).first()
		except Exception as e:
			res = None
			print(e)
		finally:
			db.session.close()
		return res

	def get_user_by_id(self):
		try:
			res = db.session.query(User).filter(User.id == self.id).first()
		except Exception as e:
			res = None
			print(e)
		finally:
			db.session.close()
		return res

	def update(self, obj):
		return ''

	def hash_password(self,	password):
		try:
			return pbkdf2_sha256.hash(password)
		except Exception as e:
			print("Erro	ao criptografar senha %s" % e)

	def set_password(self, password):
		self.password = pbkdf2_sha256.hash(password)

	def verify_password(self, password_no_hash, password_database):
		try:
			return pbkdf2_sha256.verify(password_no_hash, password_database)
		except ValueError:
			return False

	def get_total_users(self):
		try:
			res = db.session.query(func.count(User.id)).first()
		except Exception as e:
			res = []
			print(e)
		finally:
			db.session.close()
		return res
