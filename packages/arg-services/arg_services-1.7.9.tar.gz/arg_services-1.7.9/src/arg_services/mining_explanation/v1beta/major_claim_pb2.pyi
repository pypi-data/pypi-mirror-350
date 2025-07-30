from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MajorClaimRequest(_message.Message):
    __slots__ = ("language", "major_claims", "extras")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    MAJOR_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    language: str
    major_claims: _containers.RepeatedScalarFieldContainer[str]
    extras: _struct_pb2.Struct
    def __init__(self, language: _Optional[str] = ..., major_claims: _Optional[_Iterable[str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class MajorClaimResponse(_message.Message):
    __slots__ = ("major_claims", "extras")
    MAJOR_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    major_claims: _containers.RepeatedCompositeFieldContainer[MajorClaimResult]
    extras: _struct_pb2.Struct
    def __init__(self, major_claims: _Optional[_Iterable[_Union[MajorClaimResult, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class MajorClaimResult(_message.Message):
    __slots__ = ("similarities", "keywords")
    class SimilaritiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    SIMILARITIES_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    similarities: _containers.ScalarMap[str, float]
    keywords: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, similarities: _Optional[_Mapping[str, float]] = ..., keywords: _Optional[_Iterable[bool]] = ...) -> None: ...
