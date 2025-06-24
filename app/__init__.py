from flask import Flask
from config import Config

# Cria a instância da aplicação Flask
app = Flask(__name__)

# Carrega as configurações a partir da classe Config
app.config.from_object(Config)

# Importa as rotas para que o Flask as conheça
from app import routes