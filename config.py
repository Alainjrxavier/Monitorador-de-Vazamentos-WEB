import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    HIBP_API_KEY = os.environ.get('HIBP_API_KEY')

    # Configuração de Banco de Dados
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- CONFIGURAÇÃO DE CACHE (ADICIONADA) ---
    CACHE_TYPE = 'SimpleCache'  # Usa um cache simples em memória
    CACHE_DEFAULT_TIMEOUT = 3600  # Salva cada resultado por 1 hora (3600 segundos)