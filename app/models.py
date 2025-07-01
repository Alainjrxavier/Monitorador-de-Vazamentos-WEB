# app/models.py

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # <-- ESTA É A LINHA QUE FALTAVA

class User(UserMixin, db.Model):
    """Define a estrutura da tabela de usuários e seus métodos."""
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(80), nullable=False, default='user')
    monitored_emails = db.relationship('MonitoredEmail', backref='owner', lazy='dynamic')

    def set_password(self, password):
        """Cria um hash seguro para a senha fornecida."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Define como o objeto de usuário será representado em prints e logs."""
        return f'<User {self.email}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# No final de app/models.py

class MonitoredEmail(db.Model):
    """Define a estrutura da tabela de e-mails monitorados."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, nullable=False)
    # Chave estrangeira para ligar este e-mail a um usuário específico
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<MonitoredEmail {self.email}>'

