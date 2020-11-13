from flask_wtf import FlaskForm
from flask import request
from flask_sqlalchemy import SQLAlchemy
from model.Types_reg import TypesReg
from model.Department import Department
from model.Department import *
from wtforms import validators
from wtforms.fields import (
    StringField, RadioField,
    SelectField,
    SubmitField,
    DateTimeField, TextAreaField
)
from wtforms_sqlalchemy.fields import QuerySelectField


def escolha_tipo():
    return TypesReg.query


def escolha_setor_a():
    return Department.query.filter(Department.tipo == 1).all()


class FormCadastro(FlaskForm):
    num_reg = StringField('Número de Registro')
    tipo_reg = QuerySelectField('Tipo de Documento', query_factory=escolha_tipo, allow_blank=True, get_label='name')
    objeto = TextAreaField('Objeto')
    origem = QuerySelectField('Origem', query_factory=escolha_setor_a, allow_blank=True, get_label='name')
    tipo_destino = RadioField('Tipo de destino', choices=[('1', 'Interno'), ('2', 'Externo')], coerce=int,
                              id='RadioTipoDestino')
    destino = SelectField('Destino', choices=[])
    date_criacao = DateTimeField('Data de Criação')
    solicitante = SelectField('Solicitante', choices=[('0', ''), ('1', 'Interno'), ('2', 'Externo')], coerce=int)
    criador = StringField('Criado por:')
    botao1 = SubmitField('Salvar')
