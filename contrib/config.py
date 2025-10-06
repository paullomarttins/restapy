import msal
import decouple
import requests

from restapp.models import ListaWorkspaces
from contrib.get_token import obter_token

config = decouple.AutoConfig('.')

client_id = config('CLIENT_ID')
secret_id = config('CLIENT_SECRET')
tenant_id = config('TENANT_ID')
username = config('USERNAME')
password = config('PASSWORD')
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ["https://analysis.windows.net/powerbi/api/.default"]

# Chama a função que gera o token para a variável access_token
access_token = obter_token(
    username= username,
    password= password,
    tenant_id= authority,
    client_id= client_id,
    scopes= scopes,
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
        url = f'https://api.powerbi.com/v1.0/myorg/admin/groups/{workspace}/users'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'identifier': email,
            'groupUserAccessRight': perfil,
            'principalType': 'User'
        }

        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        return response.status_code, response
    except requests.exceptions.RequestException as e:
        return f'Erro de requisição: {e}'
