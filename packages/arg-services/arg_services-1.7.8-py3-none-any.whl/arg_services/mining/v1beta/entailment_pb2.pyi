from arg_services.mining.v1beta import adu_pb2 as _adu_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntailmentContextType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTAILMENT_CONTEXT_TYPE_UNSPECIFIED: _ClassVar[EntailmentContextType]
    ENTAILMENT_CONTEXT_TYPE_PARENT: _ClassVar[EntailmentContextType]
    ENTAILMENT_CONTEXT_TYPE_CHILD: _ClassVar[EntailmentContextType]
    ENTAILMENT_CONTEXT_TYPE_SIBLING: _ClassVar[EntailmentContextType]

class EntailmentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTAILMENT_TYPE_UNSPECIFIED: _ClassVar[EntailmentType]
    ENTAILMENT_TYPE_ENTAILMENT: _ClassVar[EntailmentType]
    ENTAILMENT_TYPE_CONTRADICTION: _ClassVar[EntailmentType]
    ENTAILMENT_TYPE_NEUTRAL: _ClassVar[EntailmentType]
ENTAILMENT_CONTEXT_TYPE_UNSPECIFIED: EntailmentContextType
ENTAILMENT_CONTEXT_TYPE_PARENT: EntailmentContextType
ENTAILMENT_CONTEXT_TYPE_CHILD: EntailmentContextType
ENTAILMENT_CONTEXT_TYPE_SIBLING: EntailmentContextType
ENTAILMENT_TYPE_UNSPECIFIED: EntailmentType
ENTAILMENT_TYPE_ENTAILMENT: EntailmentType
ENTAILMENT_TYPE_CONTRADICTION: EntailmentType
ENTAILMENT_TYPE_NEUTRAL: EntailmentType

class EntailmentsRequest(_message.Message):
    __slots__ = ("language", "adus", "query", "extras")
    class AdusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _adu_pb2.Segment
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_adu_pb2.Segment, _Mapping]] = ...) -> None: ...
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    ADUS_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    language: str
    adus: _containers.MessageMap[str, _adu_pb2.Segment]
    query: _containers.RepeatedCompositeFieldContainer[EntailmentQuery]
    extras: _struct_pb2.Struct
    def __init__(self, language: _Optional[str] = ..., adus: _Optional[_Mapping[str, _adu_pb2.Segment]] = ..., query: _Optional[_Iterable[_Union[EntailmentQuery, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class EntailmentsResponse(_message.Message):
    __slots__ = ("entailments", "extras")
    ENTAILMENTS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    entailments: _containers.RepeatedCompositeFieldContainer[Entailment]
    extras: _struct_pb2.Struct
    def __init__(self, entailments: _Optional[_Iterable[_Union[Entailment, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class EntailmentQuery(_message.Message):
    __slots__ = ("premise_id", "claim_id", "context")
    PREMISE_ID_FIELD_NUMBER: _ClassVar[int]
    CLAIM_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    premise_id: str
    claim_id: str
    context: _containers.RepeatedCompositeFieldContainer[EntailmentContext]
    def __init__(self, premise_id: _Optional[str] = ..., claim_id: _Optional[str] = ..., context: _Optional[_Iterable[_Union[EntailmentContext, _Mapping]]] = ...) -> None: ...

class EntailmentContext(_message.Message):
    __slots__ = ("adu_id", "weight", "type")
    ADU_ID_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    adu_id: str
    weight: float
    type: EntailmentContextType
    def __init__(self, adu_id: _Optional[str] = ..., weight: _Optional[float] = ..., type: _Optional[_Union[EntailmentContextType, str]] = ...) -> None: ...

class Entailment(_message.Message):
    __slots__ = ("type", "predictions", "premise_id", "claim_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    PREMISE_ID_FIELD_NUMBER: _ClassVar[int]
    CLAIM_ID_FIELD_NUMBER: _ClassVar[int]
    type: EntailmentType
    predictions: _containers.RepeatedCompositeFieldContainer[EntailmentPrediction]
    premise_id: str
    claim_id: str
    def __init__(self, type: _Optional[_Union[EntailmentType, str]] = ..., predictions: _Optional[_Iterable[_Union[EntailmentPrediction, _Mapping]]] = ..., premise_id: _Optional[str] = ..., claim_id: _Optional[str] = ...) -> None: ...

class EntailmentPrediction(_message.Message):
    __slots__ = ("probability", "type")
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    probability: float
    type: EntailmentType
    def __init__(self, probability: _Optional[float] = ..., type: _Optional[_Union[EntailmentType, str]] = ...) -> None: ...
