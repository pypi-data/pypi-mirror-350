from arg_services.graph.v1 import graph_pb2 as _graph_pb2
from arg_services.mining.v1beta import adu_pb2 as _adu_pb2
from arg_services.mining.v1beta import entailment_pb2 as _entailment_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GraphConstructionRequest(_message.Message):
    __slots__ = ("language", "adus", "major_claim_id", "entailments", "extras")
    class AdusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _adu_pb2.Segment
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_adu_pb2.Segment, _Mapping]] = ...) -> None: ...
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    ADUS_FIELD_NUMBER: _ClassVar[int]
    MAJOR_CLAIM_ID_FIELD_NUMBER: _ClassVar[int]
    ENTAILMENTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    language: str
    adus: _containers.MessageMap[str, _adu_pb2.Segment]
    major_claim_id: str
    entailments: _containers.RepeatedCompositeFieldContainer[_entailment_pb2.Entailment]
    extras: _struct_pb2.Struct
    def __init__(self, language: _Optional[str] = ..., adus: _Optional[_Mapping[str, _adu_pb2.Segment]] = ..., major_claim_id: _Optional[str] = ..., entailments: _Optional[_Iterable[_Union[_entailment_pb2.Entailment, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GraphConstructionResponse(_message.Message):
    __slots__ = ("graph", "extras")
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    extras: _struct_pb2.Struct
    def __init__(self, graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
