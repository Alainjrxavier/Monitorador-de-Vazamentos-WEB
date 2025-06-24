import os
from dotenv import load_dotenv

# Define o caminho base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(basedir, 'key.env'))

class Config:
    """Define as configurações da aplicação."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    HIBP_API_KEY = os.environ.get('HIBP_API_KEY')