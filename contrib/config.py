from msal import PublicClientApplication
from decouple import config
import requests

from restapp.models import ListaWorkspaces

client_id = config('CLIENT_ID')
secret_id = config('CLIENT_SECRET')
tenant_id = config('TENANT_ID')
username = config('USERNAME')
password = config('PASSWORD')

def obter_token(username, password, tenant_id, client_id, scopes):
    token_response = None
    app = PublicClientApplication(client_id, authority=tenant_id)
    token_response = app.acquire_token_by_username_password(username, password, scopes)

    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        print('Erro ao retornar Token:')
        for key, value in token_response.items():
            print(f'{key}: {value}')
        return None

# Chama a função que gera o token para a variável access_token
access_token = obter_token(
    username= username,
    password= password,
    tenant_id=f"https://login.microsoftonline.com/{tenant_id}",
    client_id= client_id,
    scopes=["https://analysis.windows.net/powerbi/api/.default"],
)

def lista_workspace():
    url = 'https://api.powerbi.com/v1.0/myorg/groups'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code == 200:
        relatorios = response.json().get('value', [])

        for item in relatorios:
            ListaWorkspaces.objects.get_or_create(
                id_ws = item['id'],
                type = item['type'],
                name = item['name']
            )
    return response

def adiciona_user_workspace(email, perfil, workspace):
    try:
        url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace}/users'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'identifier': email,
            'groupUserAccessRight': perfil,
            'principalType': 'User'
        }

        response = requests.put(url, json=params, headers=headers)
        response.raise_for_status()
        return response.status_code, response
    except requests.exceptions.RequestException as e:
        return f'Erro de requisição: {e}'
