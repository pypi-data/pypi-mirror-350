import getpass
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

import boto3
import botocore.exceptions
import grpc
import radiens.utils.constants as constants
import radiens.utils.util as util
from grpc_interceptor import ClientCallDetails, ClientInterceptor
from radiens.exceptions.grpc_error import handle_grpc_error
from radiens.grpc_radiens import (allegoserver_pb2_grpc, common_pb2,
                                  radiensserver_pb2_grpc)
from radiens.utils.enums import ClientType


class MetadataClientInterceptor(ClientInterceptor):
    def __init__(self, id_token=None, device_uuid=None):
        self._id_token = id_token
        self._device_uuid = device_uuid

    def intercept(self, method, request, call_details):
        authorization = None
        if self._id_token is not None:
            authorization = f"Bearer {self._id_token}"
        elif self._device_uuid is not None:
            authorization = f"deviceUUID {self._device_uuid}"

        # replace the authorization metadata if it exists
        new_metadata = list(
            call_details.metadata) if call_details.metadata else []
        new_metadata = [(key, value) for key,
                        value in new_metadata if key.lower() != "authorization"]
        new_metadata.append(("authorization", authorization))

        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            new_metadata,
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request, new_details)


def generate_hardware_uuid() -> str:
    """Retrieve the hardware UUID for macOS, Windows, and Linux."""
    system = platform.system()

    if system == "Darwin":
        return get_macos_hardware_uuid()
    elif system == "Windows":
        return get_windows_hardware_uuid()
    else:
        print(f"Unsupported OS: {system}", file=sys.stderr)
        return ""


def get_macos_hardware_uuid() -> str:
    """Retrieve the hardware UUID on macOS."""
    try:
        output = subprocess.check_output(
            ["ioreg", "-d2", "-c", "IOPlatformExpertDevice"], encoding="utf-8"
        )
    except subprocess.CalledProcessError as e:
        print("Failed to run ioreg:", e, file=sys.stderr)
        return ""

    match = re.search(r'"IOPlatformUUID"\s=\s"([^"]+)"', output)
    return match.group(1) if match else ""


def run_wmic_command(command: list) -> str:
    """Run a WMIC command and extract the relevant value."""
    try:
        output = subprocess.check_output(
            command, encoding="utf-8", stderr=subprocess.DEVNULL)
        lines = output.strip().split()
        if len(lines) > 1:
            return lines[1].strip()
    except subprocess.CalledProcessError:
        pass
    return ""


def get_windows_hardware_uuid() -> str:
    uuID = run_wmic_command(["wmic", "csproduct", "get", "UUID"])
    bios_serial = run_wmic_command(["wmic", "bios", "get", "serialnumber"])
    harddrive_serial = run_wmic_command(
        ["wmic", "DISKDRIVE", "get", "SerialNumber"])

    combined = (uuID + bios_serial + harddrive_serial).encode('utf-8')
    md5_hash = hashlib.md5(combined).hexdigest()
    return f"{md5_hash[:8]}-{md5_hash[8:12]}-{md5_hash[12:16]}-{md5_hash[16:20]}-{md5_hash[20:]}"


def get_hardware_uuid_from_server(addr: str):
    with util.new_insecure_channel(addr) as chan:
        if util.is_allego_addr(addr):
            stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        else:
            stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            res = stub.GetOfflineLicenseStatus(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        else:
            return res.hardwareUUID


class SessionMetaData():
    _instance = None
    _initialized = False

    def __new__(cls, core_addr: str = None):
        if cls._instance is None:
            if core_addr is None:
                raise ValueError(
                    "core_addr must be provided to create a new instance")
            cls._instance = super(SessionMetaData, cls).__new__(cls)
        return cls._instance

    def __init__(self, core_addr: str = None):
        if self._initialized:
            return
        self._id_token = None
        self._hardware_uid = None
        self._core_addr = core_addr
        self._force_no_token = os.getenv("RADIENS_OFFLINE") == "1"
        self._initialized = True

    def lazy_set_auth(self):
        if not self._force_no_token and self._id_token is None:
            try:
                app_dir = util.get_user_app_data_dir()
                client_id = util.get_app_client_id()
                refresh_token, device_key = load_session(client_id, app_dir)
                self._id_token = get_id_token(refresh_token, device_key)
            except botocore.exceptions.EndpointConnectionError as e:
                self._force_no_token = True
            except botocore.exceptions.ClientError as e:
                if e.response['ResponseMetadata']['HTTPStatusCode'] == 400:
                    self._force_no_token = True

        if self._id_token is None and self._hardware_uid is None:
            try:
                self._hardware_uid = get_hardware_uuid_from_server(
                    self._core_addr)
            except:
                self._hardware_uid = generate_hardware_uuid()


# ====== helpers ======


def get_id_token(refresh_token, device_key):
    if refresh_token is None or device_key is None:
        return get_id_token_password()
    if refresh_token is not None and device_key is not None:
        return get_id_token_refresh(refresh_token, device_key)
    return None


def get_id_token_refresh(refresh_token, device_key):
    client = boto3.client('cognito-idp', region_name=constants.REGION)
    auth_resp = client.initiate_auth(
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token,
            'DEVICE_KEY': device_key
        },
        ClientId=util.get_app_client_id()
    )

    client.close()
    return auth_resp['AuthenticationResult']['IdToken']


def get_id_token_password():
    _email = input('Enter user email address: ')
    _password = getpass.getpass(prompt='Enter use password: ')

    client = boto3.client('cognito-idp', region_name=constants.REGION)
    auth_resp = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': _email,
            'PASSWORD': _password
        },
        ClientId=util.get_app_client_id()
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
