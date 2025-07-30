from arg_services.graph.v1 import graph_pb2 as _graph_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RunPipelineRequest(_message.Message):
    __slots__ = ("texts", "extras")
    TEXTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    texts: _containers.RepeatedScalarFieldContainer[str]
    extras: _struct_pb2.Struct
    def __init__(self, texts: _Optional[_Iterable[str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RunPipelineResponse(_message.Message):
    __slots__ = ("graphs", "extras")
    GRAPHS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    graphs: _containers.RepeatedCompositeFieldContainer[_graph_pb2.Graph]
    extras: _struct_pb2.Struct
    def __init__(self, graphs: _Optional[_Iterable[_Union[_graph_pb2.Graph, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
