from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import func
from config import app_active, app_config
from model.User import User
from model.Types_reg import TypesReg
from model.Cargo import Cargo


config = app_config[app_active]

db = SQLAlchemy(config.APP)


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_reg = db.Column(db.String(9), unique=True, nullable=False)
    objeto = db.Column(db.String(120), nullable=True)
    origen = db.Column(db.String(20), nullable=False)
    destiny = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    requester = db.Column(db.String(40), db.ForeignKey(User.username), nullable=False)
    creator = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Integer, db.ForeignKey(TypesReg.id), nullable=False)
    tipo = relationship(TypesReg)
    criador = relationship(User)

    def get_all(self, limit):
        try:
            if limit is None:
                res = db.session.query(Documents).all()
            else:
                res = db.session.query(Documents).order_by(Documents.date_created).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    def update(self, obj):
        try:
            res = db.session.query(Documents).filter(Documents.id == self.id).update(obj)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    def __repr__(self):
        return self.num_reg

    def get_total_documents(self):
        try:
            res = db.session.query(func.count(Documents.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def get_last_documents(self):
        try:
            res = db.session.query(Documents).order_by(Documents.date_created).limit(5).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def get_documents_by_id(self):
        try:
            res = db.session.query(Documents).filter(Documents.id == self.id).first()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
        return res
