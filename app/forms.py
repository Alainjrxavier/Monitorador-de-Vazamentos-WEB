# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from markupsafe import Markup # <-- IMPORTAÇÃO ADICIONADA

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
    # --- CAMPO DE CONSENTIMENTO LGPD ADICIONADO AQUI ---
    accept_tos = BooleanField(
        Markup('Eu li e concordo com a <a href="/politica-de-privacidade">Política de Privacidade</a> e os <a href="/termos-de-servico">Termos de Serviço</a>.'),
        validators=[DataRequired(message="Você deve aceitar os termos para se cadastrar.")]
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

class DeleteAccountForm(FlaskForm):
    """Formulário para o usuário confirmar sua senha antes de deletar a conta."""
    password = PasswordField('Para confirmar, digite sua senha', validators=[DataRequired()])
    submit = SubmitField('Apagar Minha Conta Permanentemente')