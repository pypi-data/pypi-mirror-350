
import os
import re
import subprocess
from pathlib import Path
from sys import platform

import grpc
from radiens.auth import MetadataClientInterceptor, SessionMetaData
from radiens.exceptions.scan_for_server_error import (PIDParsingError,
                                                      PortParsingError,
                                                      UnexpectedTCPFormat)
from radiens.grpc_radiens import radiensserver_pb2, radiensserver_pb2_grpc
from radiens.utils.enums import RadiensService

REGION = 'us-east-1'
APP_CLIENT_ID_DEV = '1q4ugfpgijro91l1cjdhau60cq'
aPP_CLIENT_ID_PROD = '62hgblnnv0dbfrsqad03ub44td'
SERVER_NAME_WINDOWS = 'radiensserver.exe'

ERROR_COLOR_BG = 'black'
ERROR_COLOR_FG = 'red'


def is_dev():
    if os.getenv('ALLEGO_PROD') == '1' or os.getenv("RADIENS_PROD") == '1':
        return False
    return os.getenv('RADIENS_DEV') == '1'


def is_qa():
    return os.getenv('RADIENS_QA') == '1'


def get_app_client_id():
    if is_dev() or is_qa():
        return APP_CLIENT_ID_DEV
    return aPP_CLIENT_ID_PROD


def get_user_app_data_dir():
    if platform in ['linux', 'linux2']:
        return Path(Path.home(), '.config', 'radiens')
    elif platform == 'darwin':
        return Path(Path.home(), 'Library', 'Application Support', 'radiens')
    elif platform == 'win32':
        return Path(Path.home(), 'AppData', 'Roaming', 'radiens')
    else:
        return None


def get_radiens_port_dict(req: list[RadiensService] | None = None) -> dict[RadiensService, str]:
    radiens_servers = None
    if platform in ['linux', 'linux2', 'darwin']:
        radiens_servers = discover_radiens_servers_unix()
    elif platform == 'win32':
        radiens_servers = discover_radiens_servers_windows()
    else:
        return None
    _req = list(RadiensService) if req is None else req
    return extract_all_radiens_ports(radiens_servers, _req)


def extract_all_radiens_ports(server_spec: list, req: list[RadiensService]) -> dict[str, str]:

    # port dict with all values set to None
    port_dict = dict.fromkeys(RadiensService, None)

    for addr in server_spec:
        with new_server_channel(addr) as chan:
            # check if core
            try:
                stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.CORE] = addr.split(':')[1]

            # check if dev1
            try:
                stub = radiensserver_pb2_grpc.RadiensDev1Stub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.DEV] = addr.split(':')[1]

            # check if radiens-py
            try:
                stub = radiensserver_pb2_grpc.PyRadiens1Stub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.RADIENSPY] = addr.split(':')[1]

            # check if spikesorter
            try:
                stub = radiensserver_pb2_grpc.RadiensSpikeSorter1Stub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.SORTER] = addr.split(':')[1]

            # check if dash
            try:
                stub = radiensserver_pb2_grpc.DashboardsStub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.DASH] = addr.split(':')[1]

    return port_dict


def discover_radiens_servers_windows():
    server_spec = []
    proc = subprocess.run(
        ['tasklist.exe', '/FI', 'IMAGENAME eq {}'.format(SERVER_NAME_WINDOWS)], stdout=subprocess.PIPE)
    lines = proc.stdout.decode('utf-8').split('\n')
    for l in lines:
        if re.search(SERVER_NAME_WINDOWS, l) is not None:
            try:
                pid_start, pid_end = re.search(r'\d+', l).span()
                pid = int(l[pid_start:pid_end])
            except ValueError:
                raise PIDParsingError()
            else:
                ports = get_windows_server_ports(pid)
                for port in ports:
                    server_spec.append('localhost:{}'.format(port))
    return server_spec


def get_windows_server_ports(pid):
    ports = []
    proc = subprocess.run(
        ["netstat.exe", "-a", "-o", "-n", "-p", "TCP"], stdout=subprocess.PIPE)
    lines = proc.stdout.decode('utf-8').split('\n')
    for l in lines:
        if re.search(r'LISTENING\s+{}\b'.format(pid), l) is not None:
            try:
                port_start, port_end = re.search(r':\d+', l).span()
                port = int(l[port_start+1:port_end])
            except ValueError:
                raise PortParsingError()
            else:
                ports.append(port)
    return ports


def discover_radiens_servers_unix():
    server_spec = []
    proc = subprocess.run(['lsof', '-i', '-n', '-P'], stdout=subprocess.PIPE)
    lines = proc.stdout.decode('utf-8').split('\n')
    for l in lines:
        rad_proc = re.search(r'radienss', l)
        tcp_listen = re.search(r'(LISTEN)', l)
        if rad_proc is not None and tcp_listen is not None:
            ip_start = re.search(r'TCP', l).end()+1
            port_end = tcp_listen.start()-1
            try:
                ip, port = l[ip_start:port_end].split(':')
            except ValueError:
                raise UnexpectedTCPFormat()
            else:
                ip = 'localhost' if ip == '*' else ip
                server_spec.append(':'.join([ip, port]))
    return server_spec


user = SessionMetaData()


def new_server_channel(ip_address):
    chan = grpc.insecure_channel(
        ip_address,
        options=[('grpc.max_receive_message_length', -1)]
    )
    return grpc.intercept_channel(chan, MetadataClientInterceptor(user._id_token))
