import requests
import os
import time

HIBP_API_URL = 'https://haveibeenpwned.com/api/v3/'

def check_pwned_email(email):
    """
    Verifica um único e-mail nas APIs de Breaches e Pastes do HIBP de forma mais robusta.
    """
    api_key = os.environ.get('HIBP_API_KEY')
    if not api_key:
        return {'breaches': None, 'pastes': None, 'error': 'Chave da API HIBP não configurada.'}

    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'MonitorDeVazamentos-WebApp'
    }
    
    # Estrutura de retorno
    breaches_data = None
    pastes_data = None
    error_message = None

    # --- 1. Consulta de Breaches ---
    try:
        url = f"{HIBP_API_URL}breachedaccount/{email}"
        # Adicionado timeout de 10 segundos para evitar que a aplicação trave
        response = requests.get(url, headers=headers, timeout=10, params={'truncateResponse': 'false'})

        if response.status_code == 200:
            breaches_data = response.json()
        elif response.status_code == 404:
            pass  # OK, sem vazamentos encontrados.
        else:
            error_message = f"Erro ao consultar breaches (Status: {response.status_code})"

    except requests.exceptions.RequestException as e:
        error_message = f"Erro de conexão ao consultar breaches: {e}"
    
    # --- 2. Pausa Estratégica ---
    # Pausa para respeitar o rate limit ANTES da próxima chamada.
    time.sleep(1.6)

    # --- 3. Consulta de Pastes ---
    try:
        url = f"{HIBP_API_URL}pasteaccount/{email}"
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            pastes_data = response.json()
        elif response.status_code == 404:
            pass  # OK, sem pastes encontrados.
        else:
            # Adiciona o novo erro sem sobrescrever um erro anterior
            paste_error = f"Erro ao consultar pastes (Status: {response.status_code})"
            if error_message:
                error_message += f" | {paste_error}"
            else:
                error_message = paste_error

    except requests.exceptions.RequestException as e:
        conn_error = f"Erro de conexão ao consultar pastes: {e}"
        if error_message:
            error_message += f" | {conn_error}"
        else:
            error_message = conn_error

    return {
        'breaches': breaches_data,
        'pastes': pastes_data,
        'error': error_message
    }