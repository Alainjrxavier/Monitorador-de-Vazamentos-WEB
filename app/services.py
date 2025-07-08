# app/services.py

import requests
from flask import current_app
from app import cache

@cache.memoize(timeout=3600)
def check_pwned_email(email):
    """
    Verifica um único e-mail no HIBP, garantindo que a resposta completa seja solicitada.
    """
    current_app.logger.info(f"CACHE MISS: Realizando consulta na API para '{email}'")

    api_key = current_app.config.get('HIBP_API_KEY')
    if not api_key:
        return {'breaches': None, 'error': 'Chave da API HIBP não configurada.'}

    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'MonitorDeVazamentos-WebApp'
    }
    
    # PARÂMETRO PARA RECEBER A RESPOSTA COMPLETA
    params = {
        'truncateResponse': 'false'
    }
    
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    
    try:
        # Adicionado o parâmetro 'params' à chamada
        response = requests.get(url, headers=headers, timeout=10, params=params)
        
        if response.status_code == 200:
            return {'breaches': response.json(), 'error': None}
        elif response.status_code == 404:
            return {'breaches': None, 'error': None}
        else:
            return {'breaches': None, 'error': f"Erro na API (Status: {response.status_code})"}
            
    except requests.exceptions.RequestException as e:
        return {'breaches': None, 'error': f"Erro de conexão: {e}"}