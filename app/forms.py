# app/forms.py

from flask_wtf import FlaskForm
# ADICIONAMOS 'BooleanField' À LISTA DE IMPORTAÇÃO
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class EmailSearchForm(FlaskForm):
    email = StringField('E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."),
        Email(message="Por favor, insira um endereço de e-mail válido.")
    ])
    submit = SubmitField('Verificar')

class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')]
    )
    submit = SubmitField('Cadastrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este endereço de e-mail já está cadastrado.')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

 

class AddEmailForm(FlaskForm):
    """Formulário para adicionar um novo e-mail para monitoramento."""
    email = StringField('E-mail para Monitorar', validators=[DataRequired(), Email()])
    submit = SubmitField('Adicionar')