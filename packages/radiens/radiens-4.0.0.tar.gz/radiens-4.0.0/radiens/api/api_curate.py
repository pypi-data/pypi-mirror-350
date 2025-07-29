import warnings

import grpc
import numpy as np
import pandas as pd
from radiens.api.api_utils.protocols import ProtocolAPI, make_protocol_from_pb2
from radiens.exceptions.grpc_error import handle_grpc_error
from radiens.grpc_radiens import (allegoserver_pb2, allegoserver_pb2_grpc,
                                  common_pb2, datasource_pb2,
                                  radiensserver_pb2, radiensserver_pb2_grpc,
                                  spikesorter_pb2)
from radiens.lib.fsys import FileSysResponse
from radiens.utils.enums import ClientType
from radiens.utils.util import new_server_channel

# ====== life cycle ======

# file system


def dsrc_list_dir(addr, dirL: list, sort_by: str):
    sort_enum = ['date', 'name', 'size', 'type']
    if sort_by not in sort_enum:
        raise ValueError('{} must be in {}'.format(sort_by, sort_enum))

    if len(dirL) == 1:
        req = common_pb2.ListDataSourcesRequest(
            directory=dirL[0], sortBy=sort_enum.index(sort_by))
    else:
        req = common_pb2.ListDataSourcesRequest(
            directory='na', dirList=dirL, sortBy=sort_enum.index(sort_by))
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.ListDirectory(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.CURATE)
        return FileSysResponse(resp)


def dsrc_copy(addr, req: datasource_pb2.CopyRemoveDataSourceFileRequest):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.CopyDataSourceFile(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.CURATE)
        return FileSysResponse(resp)


def dsrc_remove(addr, req: datasource_pb2.CopyRemoveDataSourceFileRequest):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.RemoveDataSourceFile(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.CURATE)
        return FileSysResponse(resp)


def dsrc_move(addr, req: datasource_pb2.MoveDataSourceFileRequest):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.MoveDataSourceFile(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.CURATE)
        return FileSysResponse(resp)


def set_protocol(addr, protocol: ProtocolAPI):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.SetProtocol(protocol.as_protobuf())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.CURATE)
        return make_protocol_from_pb2(resp)


def get_protocol(addr, protocol_id: str):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetProtocol(
                common_pb2.ProtocolRequest(protocolID=protocol_id))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.CURATE)
        return make_protocol_from_pb2(resp)


def rename_protocol(addr, protocol_id: str, new_protocol_id: str):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.RenameProtocol(common_pb2.RenameProtocolRequest(
                protocolID=protocol_id, newProtocolID=new_protocol_id))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.CURATE)
        return make_protocol_from_pb2(resp)


def get_all_protocols(addr):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetAllProtocols(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.CURATE)
        protocols = []
        for p in resp.protocols:
            protocols.append(make_protocol_from_pb2(p))
        return protocols


def apply_protocol(addr, protocol_id: str):
    chan = new_server_channel(addr)
    stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
    try:
        stream = stub.ApplyProtocol(
            common_pb2.ProtocolRequest(protocolID=protocol_id))
    except grpc.RpcError as ex:
        handle_grpc_error(ex, ClientType.CURATE)
    return stream
