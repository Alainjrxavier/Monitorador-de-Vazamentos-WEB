import logging
from logging.handlers import RotatingFileHandler
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def setup_logging(app):
    log_dir = os.path.join(basedir, 'logs')
    
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    log_file = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info('Aplicação iniciada e logger configurado.')