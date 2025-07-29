from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SuitabilityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUITABILITY_TYPE_UNSPECIFIED: _ClassVar[SuitabilityType]
    SUITABILITY_TYPE_NO_EXPERT: _ClassVar[SuitabilityType]
    SUITABILITY_TYPE_SOMEWHAT_EXPERT: _ClassVar[SuitabilityType]
    SUITABILITY_TYPE_ABSOLUTE_EXPERT: _ClassVar[SuitabilityType]
SUITABILITY_TYPE_UNSPECIFIED: SuitabilityType
SUITABILITY_TYPE_NO_EXPERT: SuitabilityType
SUITABILITY_TYPE_SOMEWHAT_EXPERT: SuitabilityType
SUITABILITY_TYPE_ABSOLUTE_EXPERT: SuitabilityType

class ExpertSuitableRequest(_message.Message):
    __slots__ = ("premise", "scholar_id", "features", "extras")
    class FeaturesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PREMISE_FIELD_NUMBER: _ClassVar[int]
    SCHOLAR_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    premise: str
    scholar_id: str
    features: _containers.ScalarMap[str, str]
    extras: _struct_pb2.Struct
    def __init__(self, premise: _Optional[str] = ..., scholar_id: _Optional[str] = ..., features: _Optional[_Mapping[str, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ExpertSuitableResponse(_message.Message):
    __slots__ = ("type", "predictions", "extras")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    type: SuitabilityType
    predictions: _containers.RepeatedCompositeFieldContainer[SuitabilityPrediction]
    extras: _struct_pb2.Struct
    def __init__(self, type: _Optional[_Union[SuitabilityType, str]] = ..., predictions: _Optional[_Iterable[_Union[SuitabilityPrediction, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SuitabilityPrediction(_message.Message):
    __slots__ = ("probability", "type")
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    probability: float
    type: SuitabilityType
    def __init__(self, probability: _Optional[float] = ..., type: _Optional[_Union[SuitabilityType, str]] = ...) -> None: ...
