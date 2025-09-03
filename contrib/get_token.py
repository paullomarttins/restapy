from decouple import config
import msal

global_token_cache = msal.TokenCache()

# Create a preferably long-lived app instance, to avoid the overhead of app creation
global_app = msal.ConfidentialClientApplication(
    config('CLIENT_ID'),
    authority=config('AUTHORITY'),  # For Entra ID or External ID
    client_credential=config('CLIENT_SECRET'),  # ENV VAR contains a JSON blob as a string
    token_cache=global_token_cache,
    )
scopes = config("SCOPE", "").split()

def acquire_and_use_token():
    result = global_app.acquire_token_for_client(scopes=scopes)

    if 'access_token' in result:
        # print(result['access_token'])
        return result['access_token']
    else:
        print('Erro ao retornar Token:')
        for key, value in result.items():
            print(f'{key}: {value}')
        return None

# while True:  # Here we mimic a long-lived daemon
#     acquire_and_use_token()
#     print("Press Ctrl-C to stop.")
#     time.sleep(5)  # Let's say your app would run a workload every X minutes
