from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PremiseConvincingness(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PREMISE_CONVINCINGNESS_UNSPECIFIED: _ClassVar[PremiseConvincingness]
    PREMISE_CONVINCINGNESS_PREMISE_1: _ClassVar[PremiseConvincingness]
    PREMISE_CONVINCINGNESS_PREMISE_2: _ClassVar[PremiseConvincingness]
    PREMISE_CONVINCINGNESS_PREMISE_EQUAL: _ClassVar[PremiseConvincingness]
PREMISE_CONVINCINGNESS_UNSPECIFIED: PremiseConvincingness
PREMISE_CONVINCINGNESS_PREMISE_1: PremiseConvincingness
PREMISE_CONVINCINGNESS_PREMISE_2: PremiseConvincingness
PREMISE_CONVINCINGNESS_PREMISE_EQUAL: PremiseConvincingness

class ExplainRequest(_message.Message):
    __slots__ = ("claim", "premise1", "premise2", "extras")
    CLAIM_FIELD_NUMBER: _ClassVar[int]
    PREMISE1_FIELD_NUMBER: _ClassVar[int]
    PREMISE2_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    claim: str
    premise1: str
    premise2: str
    extras: _struct_pb2.Struct
    def __init__(self, claim: _Optional[str] = ..., premise1: _Optional[str] = ..., premise2: _Optional[str] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ExplainResponse(_message.Message):
    __slots__ = ("global_convincingness", "dimensions", "extras")
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: QualityDimension
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QualityDimension, _Mapping]] = ...) -> None: ...
    GLOBAL_CONVINCINGNESS_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    global_convincingness: PremiseConvincingness
    dimensions: _containers.MessageMap[str, QualityDimension]
    extras: _struct_pb2.Struct
    def __init__(self, global_convincingness: _Optional[_Union[PremiseConvincingness, str]] = ..., dimensions: _Optional[_Mapping[str, QualityDimension]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class QualityDimension(_message.Message):
    __slots__ = ("convincingness", "premise1", "premise2", "explanation", "methods")
    CONVINCINGNESS_FIELD_NUMBER: _ClassVar[int]
    PREMISE1_FIELD_NUMBER: _ClassVar[int]
    PREMISE2_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_FIELD_NUMBER: _ClassVar[int]
    METHODS_FIELD_NUMBER: _ClassVar[int]
    convincingness: PremiseConvincingness
    premise1: float
    premise2: float
    explanation: str
    methods: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, convincingness: _Optional[_Union[PremiseConvincingness, str]] = ..., premise1: _Optional[float] = ..., premise2: _Optional[float] = ..., explanation: _Optional[str] = ..., methods: _Optional[_Iterable[str]] = ...) -> None: ...
