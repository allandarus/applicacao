from flask_sqlalchemy import SQLAlchemy
from config import app_config, app_active

config = app_config[app_active]

db = SQLAlchemy(config.APP)


class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=True)
    description = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return self.name
