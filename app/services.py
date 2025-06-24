import requests
import os
import time # <-- 1. IMPORTAR O MÓDULO TIME

HIBP_API_URL = 'https://haveibeenpwned.com/api/v3/'

def check_pwned_email(email):
    api_key = os.environ.get('HIBP_API_KEY')
    if not api_key or api_key == '':
        return {'error': 'Chave da API HIBP não configurada no arquivo .env.'}

    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'MonitorDeVazamentos-ProjetoFaculdade'
    }
    
    results = {
        'breaches': None,
        'pastes': None,
        'error': None
    }

    try:
        # 1. Verificar vazamentos (breaches)
        breaches_url = f"{HIBP_API_URL}breachedaccount/{email}"
        response_breaches = requests.get(breaches_url, headers=headers, params={'truncateResponse': 'false'})
        
        if response_breaches.status_code == 200:
            results['breaches'] = response_breaches.json()
        elif response_breaches.status_code == 401:
            results['error'] = "Erro de autenticação (401). Verifique se sua chave da API HIBP é válida."
            return results
        elif response_breaches.status_code != 404:
            results['error'] = f"Erro inesperado ao consultar breaches: Status {response_breaches.status_code}"
            # Não retornamos aqui para ainda tentar a consulta de pastes

        # --- NOSSA SOLUÇÃO ---
        time.sleep(2) # <-- 2. ADICIONAR UMA PAUSA DE 2 SEGUNDOS
        # ---------------------

        # 2. Verificar pastes
        pastes_url = f"{HIBP_API_URL}pasteaccount/{email}"
        response_pastes = requests.get(pastes_url, headers=headers)
        
        if response_pastes.status_code == 200:
            results['pastes'] = response_pastes.json()
        elif response_pastes.status_code != 404:
             # Adiciona o erro de pastes sem apagar um possível erro anterior de breaches
             paste_error = f"Erro inesperado ao consultar pastes: Status {response_pastes.status_code}"
             if results['error']:
                 results['error'] += f" | {paste_error}"
             else:
                 results['error'] = paste_error

    except requests.exceptions.RequestException as e:
        results['error'] = f"Erro de conexão com a API: {e}"

    return results