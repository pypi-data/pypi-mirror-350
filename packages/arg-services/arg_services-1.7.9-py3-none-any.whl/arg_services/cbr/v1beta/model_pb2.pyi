from arg_services.graph.v1 import graph_pb2 as _graph_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnnotatedGraph(_message.Message):
    __slots__ = ("graph", "text")
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    text: str
    def __init__(self, graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ..., text: _Optional[str] = ...) -> None: ...

class CasebaseFilter(_message.Message):
    __slots__ = ("name", "cases", "kwargs")
    class KwargsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    CASES_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    cases: str
    kwargs: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., cases: _Optional[str] = ..., kwargs: _Optional[_Mapping[str, str]] = ...) -> None: ...
