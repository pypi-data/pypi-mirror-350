import getpass
import json
from pathlib import Path

import boto3
import radiens.utils.config as cfg
from grpc_interceptor import ClientCallDetails, ClientInterceptor


class MetadataClientInterceptor(ClientInterceptor):
    def __init__(self, id_token):
        self._id_token = id_token


    def intercept(self, method, request, call_details):
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [
                ("authorization", "Bearer " + self._id_token), 
            ],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request, new_details)



class SessionMetaData():
    def __init__(self):
        app_dir = cfg.get_user_app_data_dir()
        client_id = cfg.get_app_client_id()
        refresh_token, device_key = load_session(client_id, app_dir)
        self._id_token = get_id_token(refresh_token, device_key)



# ====== helpers ======
def get_id_token(refresh_token, device_key):
    if refresh_token is None or device_key is None:
        return get_id_token_password()
    if refresh_token is not None and device_key is not None:
        return get_id_token_refresh(refresh_token, device_key)
    return None

def get_id_token_refresh(refresh_token, device_key):
    client = boto3.client('cognito-idp', region_name=cfg.REGION)
    auth_resp = client.initiate_auth(
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token,
            'DEVICE_KEY': device_key
                },
        ClientId=cfg.get_app_client_id()
        )
    
    client.close()
    return auth_resp['AuthenticationResult']['IdToken']

def get_id_token_password():
    _email = input('Enter user email address: ')
    _password = getpass.getpass(prompt='Enter use password: ')

    client = boto3.client('cognito-idp', region_name=cfg.REGION)
    auth_resp = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': _email,
            'PASSWORD': _password
                },
        ClientId=cfg.get_app_client_id()
        )
    client.close()

    return auth_resp['AuthenticationResult']['IdToken']

def load_session(client_id, app_dir):
    file = Path(app_dir, "session.json")
    if not file.is_file() or file.stat().st_size == 0:
        return None, None
    with open(file) as fid:
        session_info = json.load(fid)
        if 'CognitoIdentityServiceProvider' in session_info.keys():
            session_info = session_info['CognitoIdentityServiceProvider']
        else:
            return None, None
    refresh_token, device_key = (None, None)   
    for _client_id, _app_client in session_info.items():
        if _client_id == client_id:
            if 'LastAuthUser' in _app_client.keys():
                user_key = _app_client['LastAuthUser']
                user_body = _app_client[user_key]
                fields = user_body.keys()
                refresh_token = user_body['refreshToken'] if 'refreshToken' in fields else None
                device_key = user_body['deviceKey'] if 'deviceKey' in fields else None

                break

    return refresh_token, device_key 






