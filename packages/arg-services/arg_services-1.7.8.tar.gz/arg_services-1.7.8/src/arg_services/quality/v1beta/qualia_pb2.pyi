from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QualiaRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUALIA_ROLE_UNSPECIFIED: _ClassVar[QualiaRole]
    QUALIA_ROLE_FORMAL: _ClassVar[QualiaRole]
    QUALIA_ROLE_CONSITIUTIVE: _ClassVar[QualiaRole]
    QUALIA_ROLE_TELIC: _ClassVar[QualiaRole]
    QUALIA_ROLE_AGENTIVE: _ClassVar[QualiaRole]
QUALIA_ROLE_UNSPECIFIED: QualiaRole
QUALIA_ROLE_FORMAL: QualiaRole
QUALIA_ROLE_CONSITIUTIVE: QualiaRole
QUALIA_ROLE_TELIC: QualiaRole
QUALIA_ROLE_AGENTIVE: QualiaRole

class QualiaAnnotationsRequest(_message.Message):
    __slots__ = ("text", "patterns", "language", "queries", "extras")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    PATTERNS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    text: str
    patterns: _containers.RepeatedCompositeFieldContainer[QualiaInputPattern]
    language: str
    queries: _containers.RepeatedScalarFieldContainer[str]
    extras: _struct_pb2.Struct
    def __init__(self, text: _Optional[str] = ..., patterns: _Optional[_Iterable[_Union[QualiaInputPattern, _Mapping]]] = ..., language: _Optional[str] = ..., queries: _Optional[_Iterable[str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class QualiaAnnotationsResponse(_message.Message):
    __slots__ = ("constituency_tree", "patterns", "extras")
    CONSTITUENCY_TREE_FIELD_NUMBER: _ClassVar[int]
    PATTERNS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    constituency_tree: str
    patterns: _containers.RepeatedCompositeFieldContainer[QualiaOutputPattern]
    extras: _struct_pb2.Struct
    def __init__(self, constituency_tree: _Optional[str] = ..., patterns: _Optional[_Iterable[_Union[QualiaOutputPattern, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class QualiaInputPattern(_message.Message):
    __slots__ = ("pattern", "role", "allowed_pos_tags")
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_POS_TAGS_FIELD_NUMBER: _ClassVar[int]
    pattern: str
    role: QualiaRole
    allowed_pos_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pattern: _Optional[str] = ..., role: _Optional[_Union[QualiaRole, str]] = ..., allowed_pos_tags: _Optional[_Iterable[str]] = ...) -> None: ...

class QualiaOutputPattern(_message.Message):
    __slots__ = ("input_pattern_match", "query_text", "qualia_text", "role")
    INPUT_PATTERN_MATCH_FIELD_NUMBER: _ClassVar[int]
    QUERY_TEXT_FIELD_NUMBER: _ClassVar[int]
    QUALIA_TEXT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    input_pattern_match: str
    query_text: str
    qualia_text: str
    role: QualiaRole
    def __init__(self, input_pattern_match: _Optional[str] = ..., query_text: _Optional[str] = ..., qualia_text: _Optional[str] = ..., role: _Optional[_Union[QualiaRole, str]] = ...) -> None: ...
