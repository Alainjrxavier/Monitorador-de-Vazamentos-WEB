from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache # <-- Importado
from config import Config
from app.logger_config import setup_logging

db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache() # <-- Instância do cache criada

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
cache.init_app(app) # <-- Cache inicializado com o app

login_manager.login_view = 'login'

setup_logging(app)

from app import routes, models