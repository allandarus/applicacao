
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import func
from migrate import Documents
from config import app_config,	app_active
from model.User import User

config = app_config[app_active]

db = SQLAlchemy(config.APP)


class TypesReg(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	description = db.Column(db.String(60), nullable=True)

	def __repr__(self):
		return self.name

	def get_total_types(self):
		try:
			res = db.session.query(func.count(TypesReg.id)).first()
		except Exception as e:
			res = []
			print(e)
		finally:
			db.session.close()
		return res
