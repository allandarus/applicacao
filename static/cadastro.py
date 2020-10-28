from wtforms import validators
from wtforms.fields import (
    StringField,
    SelectField, SelectFieldBase,
    SubmitField,
    DateTimeField, TextAreaField
)
from flask_wtf import FlaskForm


class FormCadastro(FlaskForm):
    num_reg = StringField('Número de Registro')
    tipo_reg = SelectField('Tipo de Documento')
    objeto = TextAreaField('Objeto')
    origem = SelectField('Origem')
    destino = SelectField('Destino')
    date_criacao = DateTimeField('Data de Criação')
    solicitante = SelectField('Solicitante')
    criador = StringField('Criado por:')
    btn = SubmitField('Salvar')
