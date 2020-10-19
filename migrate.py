from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import app_config, app_active
config = app_config[app_active]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=True)
    description = db.Column(db.String(100), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(260), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_update = db.Column(db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=True)
    recovery_code = db.Column(db.String(200), nullable=True)
    department = db.Column(db.String(40), nullable=False)
    active = db.Column(db.Boolean(), default=1, nullable=True)
    cargo = db.Column(db.Integer, db.ForeignKey(Cargo.id), nullable=False)


class TypesReg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=True)


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


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=True)
    description = db.Column(db.String(100), nullable=True)


if __name__ == '__main__':
    manager.run()
