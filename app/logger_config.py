# app/logger_config.py

import logging
from logging.handlers import RotatingFileHandler
import os
# --- 1. Importe nosso novo handler ---
from app.db_log_handler import DatabaseHandler

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def setup_logging(app):
    # A configuração do FileHandler (para o arquivo logs/app.log) continua a mesma
    log_dir = os.path.join(basedir, 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [%(pathname)s:%(lineno)d]')
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # --- 2. Adicione o handler do banco de dados ---
    # Boa prática: só logar no banco em modo de produção (não debug) para não poluir
    if not app.debug:
        db_handler = DatabaseHandler()
        db_handler.setLevel(logging.INFO)
        app.logger.addHandler(db_handler)
    
    # Define o nível geral do logger
    app.logger.setLevel(logging.INFO)
    
    # Log inicial que irá para o arquivo (e para o banco, se não estiver em modo debug)
    app.logger.info('Aplicação iniciada e logger configurado.')