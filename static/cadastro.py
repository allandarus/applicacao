from os import name
from flask_wtf import FlaskForm
from flask import request
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields.simple import HiddenField
from model.Types_reg import TypesReg
from model.Department import Department
from model.Department import *
from model.User import User
from wtforms.validators import InputRequired, ValidationError
from wtforms.fields import (StringField, RadioField, SelectField, SubmitField, 
DateTimeField, TextAreaField, HiddenField)
from wtforms_sqlalchemy.fields import QuerySelectField


def escolha_tipo():
    return TypesReg.query


def escolha_setor_a():
    return Department.query.filter(Department.tipo == 1).all()


def escolha_user():
    return User.query


class Length(object):
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = u'O campo precisa ter entre %i e %i caracteres.' % (min, max)
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            raise ValidationError(self.message)


length = Length


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class FormCadastro(FlaskForm):
    num_reg = StringField('Número de Registro')
    tipo_reg = QuerySelectField('Tipo de Documento', query_factory=escolha_tipo,
     allow_blank=True, get_label='name')
    objeto = TextAreaField('Objeto', validators=[InputRequired(),
     length(max=2000)])
    origem = QuerySelectField('Origem', query_factory=escolha_setor_a,
     allow_blank=True, get_label='name')
    tipo_destino = SelectField(
        'Tipo de Destino',
        choices=[('0', ''), ('1', 'Interno'), ('2', 'Externo - Fornecedores'),
         ('3', 'Externo - Orgão Governo')],
        coerce=int
    )
    destino = NonValidatingSelectField('Destino', choices=[])
    date_criacao = DateTimeField('Data de Criação')
    solicitante = QuerySelectField('Interessado', query_factory=escolha_user,
     allow_blank=True)
    criador = StringField('Criado por:')
    botao1 = SubmitField('Salvar')
    branco = HiddenField('')


def cont_reg(date_created, n_rows):

    current_year = date_created
    year_str = current_year.strftime("%Y")
    cont_reg = str(n_rows).zfill(3)
    return f'{cont_reg}/{year_str}'
