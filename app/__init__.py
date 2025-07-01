# Dentro de app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # <-- 1. Importe o LoginManager
from config import Config
from app.logger_config import setup_logging

db = SQLAlchemy()
login_manager = LoginManager() # <-- 2. Crie a instância do gerenciador de login

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app) # <-- 3. Inicialize o gerenciador com o app

login_manager.login_view = 'login' # <-- ADICIONE ESTA LINHA
# ...
setup_logging(app)

from app import routes, models