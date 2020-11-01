from flask_wtf import FlaskForm
from model.Types_reg import TypesReg
from model.Department import Department
from flask_sqlalchemy import SQLAlchemy
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
    return Department.query


def escolha_setor_b():
    if FormCadastro.tipo_destino == "Interno":
        return Department.query
    elif FormCadastro.tipo_destino == 'Externo':
        return "2"
    else:
        return "3"


class FormCadastro(FlaskForm):
    num_reg = StringField('Número de Registro')
    tipo_reg = QuerySelectField('Tipo de Documento', query_factory=escolha_tipo, allow_blank=True, get_label='name')
    objeto = TextAreaField('Objeto')
    origem = QuerySelectField('Origem', query_factory=escolha_setor_a, allow_blank=True, get_label='name')
    tipo_destino = RadioField('Tipo de destino', choices=[('Interno', 'Interno'), ('Externo', 'Externo')])
    destino = SelectField('Destino')
    date_criacao = DateTimeField('Data de Criação')
    solicitante = SelectField('Solicitante')
    criador = StringField('Criado por:')
    botao1 = SubmitField('Salvar')

    def hab_dest(self):
        if FormCadastro.tipo_destino is not 'Interno' or 'Externo':
            return FormCadastro.destino(disable=True)

