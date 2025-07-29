from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SegmentationRequest(_message.Message):
    __slots__ = ("text", "extras")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    text: str
    extras: _struct_pb2.Struct
    def __init__(self, text: _Optional[str] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SegmentationResponse(_message.Message):
    __slots__ = ("segments", "extras")
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[Segment]
    extras: _struct_pb2.Struct
    def __init__(self, segments: _Optional[_Iterable[_Union[Segment, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Segment(_message.Message):
    __slots__ = ("text", "start", "end")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    text: str
    start: int
    end: int
    def __init__(self, text: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class ClassificationRequest(_message.Message):
    __slots__ = ("segments", "extras")
    class SegmentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.ScalarMap[str, str]
    extras: _struct_pb2.Struct
    def __init__(self, segments: _Optional[_Mapping[str, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ClassificationResponse(_message.Message):
    __slots__ = ("adus", "extras")
    ADUS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    adus: _containers.RepeatedCompositeFieldContainer[Adu]
    extras: _struct_pb2.Struct
    def __init__(self, adus: _Optional[_Iterable[_Union[Adu, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Adu(_message.Message):
    __slots__ = ("segment_id", "tokens")
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    segment_id: str
    tokens: _containers.RepeatedCompositeFieldContainer[Token]
    def __init__(self, segment_id: _Optional[str] = ..., tokens: _Optional[_Iterable[_Union[Token, _Mapping]]] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ("text", "argumentative", "keyword")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTATIVE_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    text: str
    argumentative: bool
    keyword: bool
    def __init__(self, text: _Optional[str] = ..., argumentative: bool = ..., keyword: bool = ...) -> None: ...
