from msal import PublicClientApplication
from decouple import config
import requests
import json

client_id = config('CLIENT_ID')
secret_id = config('SECRET_KEY')
tenant_id = config('TENANT_ID')
username = config('USERNAME')
password = config('PASSWORD')

def obter_token(username, password, tenant_id, client_id, scopes):
    app = PublicClientApplication(client_id, authority=tenant_id)
    token_response = app.acquire_token_by_username_password(username, password, scopes)
    return token_response['access_token']

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
    relatorios = response.json().get('value', [])

    lista = json.loads(relatorios)
    for item in lista['name']:
        listas = print(item['name'])

    return listas

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
