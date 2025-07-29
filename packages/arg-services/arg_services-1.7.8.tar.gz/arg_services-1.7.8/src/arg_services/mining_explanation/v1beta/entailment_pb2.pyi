from arg_services.mining.v1beta import entailment_pb2 as _entailment_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntailmentsRequest(_message.Message):
    __slots__ = ("language", "entailments", "extras")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    ENTAILMENTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    language: str
    entailments: _containers.RepeatedCompositeFieldContainer[Entailment]
    extras: _struct_pb2.Struct
    def __init__(self, language: _Optional[str] = ..., entailments: _Optional[_Iterable[_Union[Entailment, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class EntailmentsResponse(_message.Message):
    __slots__ = ("results", "extras")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[EntailmentResult]
    extras: _struct_pb2.Struct
    def __init__(self, results: _Optional[_Iterable[_Union[EntailmentResult, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Entailment(_message.Message):
    __slots__ = ("premise", "claim", "type")
    PREMISE_FIELD_NUMBER: _ClassVar[int]
    CLAIM_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    premise: str
    claim: str
    type: _entailment_pb2.EntailmentType
    def __init__(self, premise: _Optional[str] = ..., claim: _Optional[str] = ..., type: _Optional[_Union[_entailment_pb2.EntailmentType, str]] = ...) -> None: ...

class EntailmentResult(_message.Message):
    __slots__ = ("similarities", "keywords_premise", "keywords_claim")
    class SimilaritiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    SIMILARITIES_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_PREMISE_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_CLAIM_FIELD_NUMBER: _ClassVar[int]
    similarities: _containers.ScalarMap[str, float]
    keywords_premise: _containers.RepeatedScalarFieldContainer[bool]
    keywords_claim: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, similarities: _Optional[_Mapping[str, float]] = ..., keywords_premise: _Optional[_Iterable[bool]] = ..., keywords_claim: _Optional[_Iterable[bool]] = ...) -> None: ...
