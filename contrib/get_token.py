import decouple
import msal

config = decouple.AutoConfig('.')

def obter_token(username, password, tenant_id, client_id, scopes):
    token_response = None
    app = msal.PublicClientApplication(client_id, authority=tenant_id)
    token_response = app.acquire_token_by_username_password(username, password, scopes)

    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        print('Erro ao retornar Token:')
        for key, value in token_response.items():
            print(f'{key}: {value}')
        return None
