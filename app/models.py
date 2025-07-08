# app/models.py

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """Define a estrutura da tabela de usuários e seus métodos."""
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(80), nullable=False, default='user')
    logs = db.relationship('Log', backref='user', lazy='dynamic')
    
    
    # Adicionamos o 'cascade' para garantir que os e-mails monitorados
    # sejam apagados quando o usuário for apagado.
    monitored_emails = db.relationship(
        'MonitoredEmail',
        backref='owner',
        lazy='dynamic',
        cascade="all, delete-orphan" # <-- MELHORIA ADICIONADA AQUI
    )

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

class MonitoredEmail(db.Model):
    """Define a estrutura da tabela de e-mails monitorados."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Define como o objeto de e-mail monitorado será representado."""
        return f'<MonitoredEmail {self.email}>'
    
    # No final de app/models.py
from datetime import datetime

# ... (suas classes User e MonitoredEmail continuam aqui) ...

class Log(db.Model):
    """Define a estrutura da tabela de logs de auditoria."""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    level = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Pode ser nulo para logs do sistema

    def __repr__(self):
        return f'<Log {self.timestamp}: {self.message}>'

# Também precisamos adicionar a relação inversa na classe User para facilitar as consultas.
# Dentro da classe User, adicione esta linha:
# logs = db.relationship('Log', backref='user', lazy='dynamic')