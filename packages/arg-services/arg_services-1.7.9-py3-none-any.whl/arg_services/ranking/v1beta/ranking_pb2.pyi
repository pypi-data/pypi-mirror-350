from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArgumentStance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ARGUMENT_STANCE_UNSPECIFIED: _ClassVar[ArgumentStance]
    ARGUMENT_STANCE_PRO: _ClassVar[ArgumentStance]
    ARGUMENT_STANCE_CON: _ClassVar[ArgumentStance]
ARGUMENT_STANCE_UNSPECIFIED: ArgumentStance
ARGUMENT_STANCE_PRO: ArgumentStance
ARGUMENT_STANCE_CON: ArgumentStance

class QualityRankingRequest(_message.Message):
    __slots__ = ("query", "adus", "extras")
    class AdusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    QUERY_FIELD_NUMBER: _ClassVar[int]
    ADUS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    query: str
    adus: _containers.ScalarMap[str, str]
    extras: _struct_pb2.Struct
    def __init__(self, query: _Optional[str] = ..., adus: _Optional[_Mapping[str, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class QualityRankingResponse(_message.Message):
    __slots__ = ("ranked_adus", "extras")
    RANKED_ADUS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    ranked_adus: _containers.RepeatedCompositeFieldContainer[QualityRankedAdu]
    extras: _struct_pb2.Struct
    def __init__(self, ranked_adus: _Optional[_Iterable[_Union[QualityRankedAdu, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class QualityRankedAdu(_message.Message):
    __slots__ = ("id", "text", "global_quality", "quality_dimensions", "stance", "extras")
    class QualityDimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_QUALITY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    STANCE_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    id: str
    text: str
    global_quality: float
    quality_dimensions: _containers.ScalarMap[str, float]
    stance: ArgumentStance
    extras: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., text: _Optional[str] = ..., global_quality: _Optional[float] = ..., quality_dimensions: _Optional[_Mapping[str, float]] = ..., stance: _Optional[_Union[ArgumentStance, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class StatisticalRankingRequest(_message.Message):
    __slots__ = ("query", "adus", "extras")
    class AdusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    QUERY_FIELD_NUMBER: _ClassVar[int]
    ADUS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    query: str
    adus: _containers.ScalarMap[str, str]
    extras: _struct_pb2.Struct
    def __init__(self, query: _Optional[str] = ..., adus: _Optional[_Mapping[str, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class StatisticalRankingResponse(_message.Message):
    __slots__ = ("ranked_adus", "extras")
    RANKED_ADUS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    ranked_adus: _containers.RepeatedCompositeFieldContainer[StatisticalRankedAdu]
    extras: _struct_pb2.Struct
    def __init__(self, ranked_adus: _Optional[_Iterable[_Union[StatisticalRankedAdu, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class StatisticalRankedAdu(_message.Message):
    __slots__ = ("id", "text", "score", "stance", "extras")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STANCE_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    id: str
    text: str
    score: float
    stance: ArgumentStance
    extras: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., text: _Optional[str] = ..., score: _Optional[float] = ..., stance: _Optional[_Union[ArgumentStance, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
