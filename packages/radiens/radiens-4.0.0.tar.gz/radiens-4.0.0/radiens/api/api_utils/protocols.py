import uuid
from pathlib import Path

import radiens.grpc_radiens.common_pb2 as common_pb2
from radiens.api.api_utils.util import (path_to_source_sink_transform,
                                        source_sink_transform_to_path,
                                        to_file_ext, to_radiens_file_type)


def make_protocol_from_pb2(pb_protocol: common_pb2.Protocol):
    protocol = ProtocolAPI(pb_protocol.id)
    for pb_node in pb_protocol.transformNodes:
        protocol.add_node(make_node_from_protobuf(pb_node))
    for pb_edge in pb_protocol.transformEdges:
        protocol.add_edge(make_edge_from_protobuf(pb_edge))
    return protocol


def make_node_from_protobuf(pb_node: common_pb2.TransformNode):
    if pb_node.invalid is True:
        raise ValueError(
            'node: {} -- INVALID::{}'.format(pb_node.id, pb_node.errorMessage))
    node = TransformNode(node_id=pb_node.id)
    node._invalid = pb_node.invalid
    node._err_msg = pb_node.errorMessage
    node._pos_x = pb_node.position.x
    node._pos_y = pb_node.position.y
    if pb_node.type in [common_pb2.LOWPASS_FILTER]:
        node.lowpass(pb_node.highLowPassParams.frequency)
    elif pb_node.type in [common_pb2.HIGHPASS_FILTER]:
        node.highpass(pb_node.highLowPassParams.frequency)
    elif pb_node.type in [common_pb2.BANDPASS_FILTER]:
        node.bandpass(pb_node.bandParams.lowFrequency,
                      pb_node.bandParams.highFrequency)
    elif pb_node.type in [common_pb2.BANDSTOP_FILTER]:
        node.bandstop(pb_node.bandParams.lowFrequency,
                      pb_node.bandParams.highFrequency)
    elif pb_node.type in [common_pb2.NOTCH_FILTER]:
        node.notch(pb_node.notchParams.notchFrequency,
                   pb_node.notchParams.notchBandwidth)
    elif pb_node.type in [common_pb2.PAIRED_REF]:
        node.paired_ref(pb_node.pairedRefParams.refNtvChanIdx,
                        pb_node.pairedRefParams.targetNtvChanIdx)
    elif pb_node.type in [common_pb2.VIRTUAL_REF]:
        node.virtual_ref(pb_node.virtualRefParams.refNtvChanIdx)
    elif pb_node.type in [common_pb2.CAR_REF]:
        node.car()
    elif pb_node.type in [common_pb2.SLICE_TIME]:
        node.slice_time(pb_node.sliceTimeParams.timeStart,
                        pb_node.sliceTimeParams.timeEnd)
    elif pb_node.type in [common_pb2.SLICE_CHANNELS]:
        node.slice_channels(pb_node.sliceChannelsParams.sysChanIdxs)
    elif pb_node.type in [common_pb2.DOWNSAMPLE]:
        node.time_decimate(pb_node.downsampleParams.sampleFactor)
    elif pb_node.type in [common_pb2.SINK]:
        node.datasource_sink(Path(pb_node.datasourceSinkParams.path, pb_node.datasourceSinkParams.dsrcName +
                                  '.'+to_file_ext(pb_node.datasourceSinkParams.fileType)))
    elif pb_node.type in [common_pb2.SOURCE]:
        node.datasource_sink(Path(pb_node.datasourceSinkParams.path, pb_node.datasourceSinkParams.dsrcName +
                                  '.'+to_file_ext(pb_node.datasourceSinkParams.fileType)))
    else:
        raise ValueError('invalid transform node type {}'.format(pb_node.type))
    return node


def make_edge_from_protobuf(pb_edge: common_pb2.TransformEdge):
    return TransformEdge(edge_id=pb_edge.id, src_node_id=pb_edge.source, targ_node_id=pb_edge.target)


class TransformNode:
    def __init__(self, node_id: str):
        self._node_id = node_id
        self._node_type = None
        self._pos_x = 0
        self._pos_y = 0
        self._invalid = False
        self._err_msg = ''
        self._params = {}

    @ property
    def id(self):
        return self._node_id

    @ property
    def node_type(self):
        return self._node_type

    @ property
    def invalid(self):
        return self._invalid

    @ property
    def err_msg(self):
        return self._err_msg

    @ property
    def params(self):
        return self._params

    def lowpass(self, freq: float):
        self._node_type = common_pb2.LOWPASS_FILTER
        self._params['highLowPass'] = {'frequency': freq}
        return self

    def highpass(self, freq: float):
        self._node_type = common_pb2.HIGHPASS_FILTER
        self._params['highLowPass'] = {'frequency': freq}
        return self

    def bandpass(self, low_freq: float, high_freq: float):
        self._node_type = common_pb2.BANDPASS_FILTER
        self._params['band'] = {
            'lowFrequency': low_freq, 'highFrequency': high_freq}
        return self

    def bandstop(self, low_freq: float, high_freq: float):
        self._node_type = common_pb2.BANDSTOP_FILTER
        self._params['band'] = {
            'lowFrequency': low_freq, 'highFrequency': high_freq}
        return self

    def notch(self, freq: float, bandwidth: float):
        self._node_type = common_pb2.NOTCH_FILTER
        self._params['notch'] = {
            'notchFrequency': freq, 'notchBandwidth': bandwidth}
        return self

    def paired_ref(self, ref_ntv_chan_idx: int, target_ntv_chan_idx: int):
        self._node_type = common_pb2.PAIRED_REF
        self._params['pairedRef'] = {
            'refNtvChanIdx': ref_ntv_chan_idx, 'targetNtvChanIdx': target_ntv_chan_idx}
        return self

    def virtual_ref(self, ref_ntv_chan_idx: int):
        self._node_type = common_pb2.VIRTUAL_REF
        self._params['virtualRef'] = {'refNtvChanIdx': ref_ntv_chan_idx}
        return self

    def car(self):
        self._node_type = common_pb2.CAR_REF
        self._params['car'] = {}
        return self

    def slice_time(self, time_start: float, time_end: float):
        self._node_type = common_pb2.SLICE_TIME
        self._params['sliceTime'] = {
            'timeStart': time_start, 'timeEnd': time_end}
        return self

    def slice_channels(self, sys_chan_idxs: list):
        self._node_type = common_pb2.SLICE_CHANNELS
        self._params['sliceChannels'] = {'sysChanIdxs': sys_chan_idxs}
        return self

    def time_decimate(self, sample_factor: int):
        self._node_type = common_pb2.DOWNSAMPLE
        self._params['downsample'] = {'sampleFactor': sample_factor}
        return self

    def datasource_sink(self, path: Path):
        self._node_type = common_pb2.SINK
        self._params['datasourceSink'] = {'dsrcName': path.expanduser().resolve().stem,
                                          'path': str(path.expanduser().resolve().parent), 'fileType': to_radiens_file_type(path)}
        return self

    def datasource_source(self, path: Path):
        self._node_type = common_pb2.SOURCE
        self._params['datasourceSink'] = {'dsrcName': path.expanduser().resolve().stem,
                                          'path': str(path.expanduser().resolve().parent), 'fileType': to_radiens_file_type(path)}
        return self

    def as_protobuf(self):
        if self._node_type in [common_pb2.LOWPASS_FILTER, common_pb2.HIGHPASS_FILTER]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            highLowPassParams=common_pb2.HighLowPassTransformParams(
                                                frequency=self._params['highLowPass']['frequency']))
        if self._node_type in [common_pb2.BANDPASS_FILTER, common_pb2.BANDSTOP_FILTER]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            bandParams=common_pb2.BandTransformParams(
                                                lowFrequency=self._params['band']['lowFrequency'], highFrequency=self._params['band']['highFrequency']))
        if self._node_type in [common_pb2.NOTCH_FILTER]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            notchParams=common_pb2.NotchTransformParams(notchFrequency=self._params['notch']['notchFrequency'], notchBandwidth=self._params['notch']['notchBandwidth']))
        if self._node_type in [common_pb2.PAIRED_REF]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            pairedRefParams=common_pb2.PairedRefTransformParams(refNtvChanIdx=self._params['pairedRef']['refNtvChanIdx'], targetNtvChanIdx=self._params['pairedRef']['targetNtvChanIdx']))
        if self._node_type in [common_pb2.VIRTUAL_REF]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            virtualRefParams=common_pb2.VirtualRefTransformParams(refNtvChanIdx=self._params['virtualRef']['refNtvChanIdx']))
        if self._node_type in [common_pb2.CAR_REF]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            carParams=common_pb2.CARTransformParams())
        if self._node_type in [common_pb2.SLICE_TIME]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            sliceTimeParams=common_pb2.SliceTimeTransformParams(timeStart=self._params['sliceTime']['timeStart'], timeEnd=self._params['sliceTime']['timeEnd']))
        if self._node_type in [common_pb2.SLICE_CHANNELS]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            sliceChannelsParams=common_pb2.SliceChannelsTransformParams(sysChanIdxs=self._params['sliceChannels']['sysChanIdxs']))
        if self._node_type in [common_pb2.DOWNSAMPLE]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            downsampleParams=common_pb2.DownsampleTransformParams(sampleFactor=self._params['downsample']['sampleFactor']))
        if self._node_type in [common_pb2.SINK, common_pb2.SOURCE]:
            return common_pb2.TransformNode(id=self._node_id, type=self._node_type, invalid=False,
                                            datasourceSinkParams=common_pb2.DataSourceSinkTransformParams(dsrcName=self._params['datasourceSink']['dsrcName'], path=self._params['datasourceSink']['path'], fileType=self._params['datasourceSink']['fileType']))
        raise ValueError(
            'invalid transform node type {}'.format(self._node_type))


class TransformEdge:
    def __init__(self, edge_id: str, src_node_id: str, targ_node_id: str):
        self._edge_id = edge_id
        self._src_node_id = src_node_id
        self._targ_node_id = targ_node_id

    @ property
    def id(self):
        return self._edge_id

    @ property
    def source_node_id(self):
        return self._src_node_id

    @ property
    def target_node_id(self):
        return self._targ_node_id

    def as_protobuf(self):
        return common_pb2.TransformEdge(id=self._edge_id, source=self.source_node_id, target=self.target_node_id)


class ProtocolAPI:
    def __init__(self, protocol_id: str):
        self._protocol_id = '{}__{}'.format(
            protocol_id, str(uuid.uuid4())[4:13])
        self._transform_nodes = {}
        self._transform_edges = {}

    @ property
    def id(self):
        return self._protocol_id

    @ property
    def nodes(self):
        return self._transform_nodes

    @ property
    def edges(self):
        return self._transform_edges

    def add_node(self, node: TransformNode):
        if node.id in self._transform_nodes.keys():
            raise ValueError('{} node id already exists'.format(node.id))
        self._transform_nodes[node.id] = node
        return self

    def add_edge(self, edge: TransformEdge):
        if edge.id in self._transform_edges.keys():
            raise ValueError('{} edge id already exists'.format(edge.id))
        self._transform_edges[edge.id] = edge
        return self

    def as_protobuf(self):
        pb_edges = []
        for _, edge in self._transform_edges.items():
            pb_edges.append(edge.as_protobuf())
        pb_nodes = []
        for _, node in self._transform_nodes.items():
            pb_nodes.append(node.as_protobuf())
        return common_pb2.Protocol(id=self._protocol_id, transformNodes=pb_nodes, transformEdges=pb_edges)
