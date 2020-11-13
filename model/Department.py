from flask_sqlalchemy import SQLAlchemy
from config import app_config, app_active

config = app_config[app_active]

db = SQLAlchemy(config.APP)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=True)
    tipo = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return self.name

    def get_all_department(self, limit):
        try:
            if limit is None:
                res = db.session.query(Department).all()
            else:
                res = db.session.query(Department).order_by(Department.date_created).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def get_department_by_tipo(self):
        try:
            res = db.session.query(Department).filter(Department.tipo == self.tipo).first()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
        return res
