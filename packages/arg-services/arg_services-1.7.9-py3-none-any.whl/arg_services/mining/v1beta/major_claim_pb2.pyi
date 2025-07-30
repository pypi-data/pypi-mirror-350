from arg_services.mining.v1beta import adu_pb2 as _adu_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MajorClaimRequest(_message.Message):
    __slots__ = ("language", "segments", "limit", "extras")
    class SegmentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _adu_pb2.Segment
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_adu_pb2.Segment, _Mapping]] = ...) -> None: ...
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    language: str
    segments: _containers.MessageMap[str, _adu_pb2.Segment]
    limit: int
    extras: _struct_pb2.Struct
    def __init__(self, language: _Optional[str] = ..., segments: _Optional[_Mapping[str, _adu_pb2.Segment]] = ..., limit: _Optional[int] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class MajorClaimResponse(_message.Message):
    __slots__ = ("ranking", "extras")
    RANKING_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    ranking: _containers.RepeatedCompositeFieldContainer[MajorClaimResult]
    extras: _struct_pb2.Struct
    def __init__(self, ranking: _Optional[_Iterable[_Union[MajorClaimResult, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class MajorClaimResult(_message.Message):
    __slots__ = ("id", "probability")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    probability: float
    def __init__(self, id: _Optional[str] = ..., probability: _Optional[float] = ...) -> None: ...
