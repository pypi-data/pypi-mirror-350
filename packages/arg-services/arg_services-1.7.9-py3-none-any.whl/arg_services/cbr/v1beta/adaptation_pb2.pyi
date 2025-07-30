from arg_services.cbr.v1beta import model_pb2 as _model_pb2
from arg_services.cbr.v1beta import retrieval_pb2 as _retrieval_pb2
from arg_services.nlp.v1 import nlp_pb2 as _nlp_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTION_UNSPECIFIED: _ClassVar[Direction]
    DIRECTION_GENERALIZATION: _ClassVar[Direction]
    DIRECTION_SPECIALIZATION: _ClassVar[Direction]
    DIRECTION_COMBINED: _ClassVar[Direction]

class Pos(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POS_UNSPECIFIED: _ClassVar[Pos]
    POS_NOUN: _ClassVar[Pos]
    POS_VERB: _ClassVar[Pos]
    POS_ADJECTIVE: _ClassVar[Pos]
    POS_ADVERB: _ClassVar[Pos]
DIRECTION_UNSPECIFIED: Direction
DIRECTION_GENERALIZATION: Direction
DIRECTION_SPECIALIZATION: Direction
DIRECTION_COMBINED: Direction
POS_UNSPECIFIED: Pos
POS_NOUN: Pos
POS_VERB: Pos
POS_ADJECTIVE: Pos
POS_ADVERB: Pos

class AdaptRequest(_message.Message):
    __slots__ = ("cases", "query", "nlp_config", "direction", "extras")
    class CasesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AdaptedCaseRequest
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AdaptedCaseRequest, _Mapping]] = ...) -> None: ...
    CASES_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    NLP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    cases: _containers.MessageMap[str, AdaptedCaseRequest]
    query: _model_pb2.AnnotatedGraph
    nlp_config: _nlp_pb2.NlpConfig
    direction: Direction
    extras: _struct_pb2.Struct
    def __init__(self, cases: _Optional[_Mapping[str, AdaptedCaseRequest]] = ..., query: _Optional[_Union[_model_pb2.AnnotatedGraph, _Mapping]] = ..., nlp_config: _Optional[_Union[_nlp_pb2.NlpConfig, _Mapping]] = ..., direction: _Optional[_Union[Direction, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class AdaptResponse(_message.Message):
    __slots__ = ("cases", "extras")
    class CasesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AdaptedCaseResponse
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AdaptedCaseResponse, _Mapping]] = ...) -> None: ...
    CASES_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    cases: _containers.MessageMap[str, AdaptedCaseResponse]
    extras: _struct_pb2.Struct
    def __init__(self, cases: _Optional[_Mapping[str, AdaptedCaseResponse]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class AdaptedCaseRequest(_message.Message):
    __slots__ = ("case", "rules", "mapping")
    CASE_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    MAPPING_FIELD_NUMBER: _ClassVar[int]
    case: _model_pb2.AnnotatedGraph
    rules: _containers.RepeatedCompositeFieldContainer[Rule]
    mapping: _retrieval_pb2.RetrievedMapping
    def __init__(self, case: _Optional[_Union[_model_pb2.AnnotatedGraph, _Mapping]] = ..., rules: _Optional[_Iterable[_Union[Rule, _Mapping]]] = ..., mapping: _Optional[_Union[_retrieval_pb2.RetrievedMapping, _Mapping]] = ...) -> None: ...

class AdaptedCaseResponse(_message.Message):
    __slots__ = ("case", "extracted_concepts", "discarded_concepts", "applied_rules", "discarded_rules", "generated_rules", "rule_candidates")
    CASE_FIELD_NUMBER: _ClassVar[int]
    EXTRACTED_CONCEPTS_FIELD_NUMBER: _ClassVar[int]
    DISCARDED_CONCEPTS_FIELD_NUMBER: _ClassVar[int]
    APPLIED_RULES_FIELD_NUMBER: _ClassVar[int]
    DISCARDED_RULES_FIELD_NUMBER: _ClassVar[int]
    GENERATED_RULES_FIELD_NUMBER: _ClassVar[int]
    RULE_CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    case: _model_pb2.AnnotatedGraph
    extracted_concepts: _containers.RepeatedCompositeFieldContainer[Concept]
    discarded_concepts: _containers.RepeatedCompositeFieldContainer[Concept]
    applied_rules: _containers.RepeatedCompositeFieldContainer[Rule]
    discarded_rules: _containers.RepeatedCompositeFieldContainer[Rule]
    generated_rules: _containers.RepeatedCompositeFieldContainer[Rule]
    rule_candidates: _containers.RepeatedCompositeFieldContainer[RuleCandidates]
    def __init__(self, case: _Optional[_Union[_model_pb2.AnnotatedGraph, _Mapping]] = ..., extracted_concepts: _Optional[_Iterable[_Union[Concept, _Mapping]]] = ..., discarded_concepts: _Optional[_Iterable[_Union[Concept, _Mapping]]] = ..., applied_rules: _Optional[_Iterable[_Union[Rule, _Mapping]]] = ..., discarded_rules: _Optional[_Iterable[_Union[Rule, _Mapping]]] = ..., generated_rules: _Optional[_Iterable[_Union[Rule, _Mapping]]] = ..., rule_candidates: _Optional[_Iterable[_Union[RuleCandidates, _Mapping]]] = ...) -> None: ...

class Rule(_message.Message):
    __slots__ = ("source", "target")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    source: Concept
    target: Concept
    def __init__(self, source: _Optional[_Union[Concept, _Mapping]] = ..., target: _Optional[_Union[Concept, _Mapping]] = ...) -> None: ...

class Concept(_message.Message):
    __slots__ = ("lemma", "pos", "score")
    LEMMA_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    lemma: str
    pos: Pos
    score: float
    def __init__(self, lemma: _Optional[str] = ..., pos: _Optional[_Union[Pos, str]] = ..., score: _Optional[float] = ...) -> None: ...

class RuleCandidates(_message.Message):
    __slots__ = ("source", "target")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    source: Concept
    target: _containers.RepeatedCompositeFieldContainer[Concept]
    def __init__(self, source: _Optional[_Union[Concept, _Mapping]] = ..., target: _Optional[_Iterable[_Union[Concept, _Mapping]]] = ...) -> None: ...
