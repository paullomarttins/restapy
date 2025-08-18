# from msal import ConfidentialClientApplication
from decouple import config

def obter_token():
    client_id = config('CLIENT_ID')
    secret_id = config('SECRET_KEY')
    tenant_id = config('TENANT_ID')

    authority = f'https://login.microsoftonline.com/{tenant_id}'
    scope = ['https://analysis.windows.net/powerbi/api/.default']

    app = ConfidentialClientApplication(client_id, authority=authority, client_crendential=secret_id)
    token_response = app.acquire_token_for_client(scopes=scope)

    return token_response.get('access_token')
