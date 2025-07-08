# app/db_log_handler.py

import logging
from flask import request
from flask_login import current_user

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        # Importamos os objetos da aplicação AQUI DENTRO para evitar erros de importação circular
        from app import app, db
        from app.models import Log

        # Criamos manualmente o contexto da aplicação
        with app.app_context():
            # Evita logar a consulta da própria página de logs para não criar um loop infinito
            if request and request.path == '/logs':
                return

            user_id = current_user.id if current_user and current_user.is_authenticated else None
            
            log_entry = Log(
                level=record.levelname,
                message=self.format(record),
                user_id=user_id
            )
            db.session.add(log_entry)
            db.session.commit()