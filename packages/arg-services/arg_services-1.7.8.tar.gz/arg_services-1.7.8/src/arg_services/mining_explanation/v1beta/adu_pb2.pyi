from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClassificationRequest(_message.Message):
    __slots__ = ("language", "segments", "extras")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    language: str
    segments: _containers.RepeatedScalarFieldContainer[str]
    extras: _struct_pb2.Struct
    def __init__(self, language: _Optional[str] = ..., segments: _Optional[_Iterable[str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ClassificationResponse(_message.Message):
    __slots__ = ("segments", "extras")
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[Segment]
    extras: _struct_pb2.Struct
    def __init__(self, segments: _Optional[_Iterable[_Union[Segment, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Segment(_message.Message):
    __slots__ = ("keyword_markers", "clauses")
    KEYWORD_MARKERS_FIELD_NUMBER: _ClassVar[int]
    CLAUSES_FIELD_NUMBER: _ClassVar[int]
    keyword_markers: _containers.RepeatedScalarFieldContainer[bool]
    clauses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keyword_markers: _Optional[_Iterable[bool]] = ..., clauses: _Optional[_Iterable[str]] = ...) -> None: ...
