from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FineGranularClusteringRequest(_message.Message):
    __slots__ = ("query", "adus", "extras")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    ADUS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    query: str
    adus: _containers.RepeatedScalarFieldContainer[str]
    extras: _struct_pb2.Struct
    def __init__(self, query: _Optional[str] = ..., adus: _Optional[_Iterable[str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class FineGranularClusteringResponse(_message.Message):
    __slots__ = ("predictions", "extras")
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    predictions: _containers.RepeatedCompositeFieldContainer[GranularityPrediction]
    extras: _struct_pb2.Struct
    def __init__(self, predictions: _Optional[_Iterable[_Union[GranularityPrediction, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GranularityPrediction(_message.Message):
    __slots__ = ("stance", "frame", "meaning", "hierarchic")
    STANCE_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    MEANING_FIELD_NUMBER: _ClassVar[int]
    HIERARCHIC_FIELD_NUMBER: _ClassVar[int]
    stance: float
    frame: float
    meaning: float
    hierarchic: float
    def __init__(self, stance: _Optional[float] = ..., frame: _Optional[float] = ..., meaning: _Optional[float] = ..., hierarchic: _Optional[float] = ...) -> None: ...
