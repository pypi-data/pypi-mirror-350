from arg_services.cbr.v1beta import model_pb2 as _model_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CasebaseRequest(_message.Message):
    __slots__ = ("include", "exclude", "extras")
    INCLUDE_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    include: _model_pb2.CasebaseFilter
    exclude: _model_pb2.CasebaseFilter
    extras: _struct_pb2.Struct
    def __init__(self, include: _Optional[_Union[_model_pb2.CasebaseFilter, _Mapping]] = ..., exclude: _Optional[_Union[_model_pb2.CasebaseFilter, _Mapping]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CasebaseResponse(_message.Message):
    __slots__ = ("cases",)
    class CasesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _model_pb2.AnnotatedGraph
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_model_pb2.AnnotatedGraph, _Mapping]] = ...) -> None: ...
    CASES_FIELD_NUMBER: _ClassVar[int]
    cases: _containers.MessageMap[str, _model_pb2.AnnotatedGraph]
    def __init__(self, cases: _Optional[_Mapping[str, _model_pb2.AnnotatedGraph]] = ...) -> None: ...
