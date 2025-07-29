from arg_services.cbr.v1beta import model_pb2 as _model_pb2
from arg_services.nlp.v1 import nlp_pb2 as _nlp_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MappingAlgorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MAPPING_ALGORITHM_UNSPECIFIED: _ClassVar[MappingAlgorithm]
    MAPPING_ALGORITHM_ASTAR: _ClassVar[MappingAlgorithm]
    MAPPING_ALGORITHM_GREEDY: _ClassVar[MappingAlgorithm]
    MAPPING_ALGORITHM_ISOMORPHISM: _ClassVar[MappingAlgorithm]
    MAPPING_ALGORITHM_HUNGARIAN: _ClassVar[MappingAlgorithm]
    MAPPING_ALGORITHM_BRUTE_FORCE: _ClassVar[MappingAlgorithm]
    MAPPING_ALGORITHM_EDIT_PATHS: _ClassVar[MappingAlgorithm]

class SchemeHandling(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCHEME_HANDLING_UNSPECIFIED: _ClassVar[SchemeHandling]
    SCHEME_HANDLING_BINARY: _ClassVar[SchemeHandling]
    SCHEME_HANDLING_TAXONOMY: _ClassVar[SchemeHandling]
    SCHEME_HANDLING_EXACT: _ClassVar[SchemeHandling]
MAPPING_ALGORITHM_UNSPECIFIED: MappingAlgorithm
MAPPING_ALGORITHM_ASTAR: MappingAlgorithm
MAPPING_ALGORITHM_GREEDY: MappingAlgorithm
MAPPING_ALGORITHM_ISOMORPHISM: MappingAlgorithm
MAPPING_ALGORITHM_HUNGARIAN: MappingAlgorithm
MAPPING_ALGORITHM_BRUTE_FORCE: MappingAlgorithm
MAPPING_ALGORITHM_EDIT_PATHS: MappingAlgorithm
SCHEME_HANDLING_UNSPECIFIED: SchemeHandling
SCHEME_HANDLING_BINARY: SchemeHandling
SCHEME_HANDLING_TAXONOMY: SchemeHandling
SCHEME_HANDLING_EXACT: SchemeHandling

class RetrieveRequest(_message.Message):
    __slots__ = ("casebase_filter", "cases", "queries", "nlp_config", "limit", "semantic_retrieval", "structural_retrieval", "mapping_algorithm", "mapping_algorithm_variant", "scheme_handling", "extras")
    class CasesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _model_pb2.AnnotatedGraph
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_model_pb2.AnnotatedGraph, _Mapping]] = ...) -> None: ...
    class QueriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _model_pb2.AnnotatedGraph
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_model_pb2.AnnotatedGraph, _Mapping]] = ...) -> None: ...
    CASEBASE_FILTER_FIELD_NUMBER: _ClassVar[int]
    CASES_FIELD_NUMBER: _ClassVar[int]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    NLP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SEMANTIC_RETRIEVAL_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_RETRIEVAL_FIELD_NUMBER: _ClassVar[int]
    MAPPING_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    MAPPING_ALGORITHM_VARIANT_FIELD_NUMBER: _ClassVar[int]
    SCHEME_HANDLING_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    casebase_filter: _model_pb2.CasebaseFilter
    cases: _containers.MessageMap[str, _model_pb2.AnnotatedGraph]
    queries: _containers.MessageMap[str, _model_pb2.AnnotatedGraph]
    nlp_config: _nlp_pb2.NlpConfig
    limit: int
    semantic_retrieval: bool
    structural_retrieval: bool
    mapping_algorithm: MappingAlgorithm
    mapping_algorithm_variant: int
    scheme_handling: SchemeHandling
    extras: _struct_pb2.Struct
    def __init__(self, casebase_filter: _Optional[_Union[_model_pb2.CasebaseFilter, _Mapping]] = ..., cases: _Optional[_Mapping[str, _model_pb2.AnnotatedGraph]] = ..., queries: _Optional[_Mapping[str, _model_pb2.AnnotatedGraph]] = ..., nlp_config: _Optional[_Union[_nlp_pb2.NlpConfig, _Mapping]] = ..., limit: _Optional[int] = ..., semantic_retrieval: bool = ..., structural_retrieval: bool = ..., mapping_algorithm: _Optional[_Union[MappingAlgorithm, str]] = ..., mapping_algorithm_variant: _Optional[int] = ..., scheme_handling: _Optional[_Union[SchemeHandling, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RetrieveResponse(_message.Message):
    __slots__ = ("query_responses", "extras")
    class QueryResponsesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: QueryResponse
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QueryResponse, _Mapping]] = ...) -> None: ...
    QUERY_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    query_responses: _containers.MessageMap[str, QueryResponse]
    extras: _struct_pb2.Struct
    def __init__(self, query_responses: _Optional[_Mapping[str, QueryResponse]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("semantic_ranking", "structural_ranking", "structural_mapping")
    SEMANTIC_RANKING_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_RANKING_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_MAPPING_FIELD_NUMBER: _ClassVar[int]
    semantic_ranking: _containers.RepeatedCompositeFieldContainer[RetrievedCase]
    structural_ranking: _containers.RepeatedCompositeFieldContainer[RetrievedCase]
    structural_mapping: _containers.RepeatedCompositeFieldContainer[RetrievedMapping]
    def __init__(self, semantic_ranking: _Optional[_Iterable[_Union[RetrievedCase, _Mapping]]] = ..., structural_ranking: _Optional[_Iterable[_Union[RetrievedCase, _Mapping]]] = ..., structural_mapping: _Optional[_Iterable[_Union[RetrievedMapping, _Mapping]]] = ...) -> None: ...

class RetrievedCase(_message.Message):
    __slots__ = ("id", "similarity", "graph")
    ID_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    id: str
    similarity: float
    graph: _model_pb2.AnnotatedGraph
    def __init__(self, id: _Optional[str] = ..., similarity: _Optional[float] = ..., graph: _Optional[_Union[_model_pb2.AnnotatedGraph, _Mapping]] = ...) -> None: ...

class RetrievedMapping(_message.Message):
    __slots__ = ("case", "node_mappings")
    CASE_FIELD_NUMBER: _ClassVar[int]
    NODE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    case: RetrievedCase
    node_mappings: _containers.RepeatedCompositeFieldContainer[MappedElement]
    def __init__(self, case: _Optional[_Union[RetrievedCase, _Mapping]] = ..., node_mappings: _Optional[_Iterable[_Union[MappedElement, _Mapping]]] = ...) -> None: ...

class MappedElement(_message.Message):
    __slots__ = ("query_id", "case_id", "similarity")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    CASE_ID_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    case_id: str
    similarity: float
    def __init__(self, query_id: _Optional[str] = ..., case_id: _Optional[str] = ..., similarity: _Optional[float] = ...) -> None: ...

class SimilaritiesRequest(_message.Message):
    __slots__ = ("cases", "query", "nlp_config", "structural", "mapping_algorithm", "mapping_algorithm_variant", "scheme_handling", "extras")
    CASES_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    NLP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_FIELD_NUMBER: _ClassVar[int]
    MAPPING_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    MAPPING_ALGORITHM_VARIANT_FIELD_NUMBER: _ClassVar[int]
    SCHEME_HANDLING_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    cases: _containers.RepeatedCompositeFieldContainer[_model_pb2.AnnotatedGraph]
    query: _model_pb2.AnnotatedGraph
    nlp_config: _nlp_pb2.NlpConfig
    structural: bool
    mapping_algorithm: MappingAlgorithm
    mapping_algorithm_variant: int
    scheme_handling: SchemeHandling
    extras: _struct_pb2.Struct
    def __init__(self, cases: _Optional[_Iterable[_Union[_model_pb2.AnnotatedGraph, _Mapping]]] = ..., query: _Optional[_Union[_model_pb2.AnnotatedGraph, _Mapping]] = ..., nlp_config: _Optional[_Union[_nlp_pb2.NlpConfig, _Mapping]] = ..., structural: bool = ..., mapping_algorithm: _Optional[_Union[MappingAlgorithm, str]] = ..., mapping_algorithm_variant: _Optional[int] = ..., scheme_handling: _Optional[_Union[SchemeHandling, str]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SimilaritiesResponse(_message.Message):
    __slots__ = ("similarities", "extras")
    SIMILARITIES_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    similarities: _containers.RepeatedCompositeFieldContainer[SimilarityResponse]
    extras: _struct_pb2.Struct
    def __init__(self, similarities: _Optional[_Iterable[_Union[SimilarityResponse, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SimilarityResponse(_message.Message):
    __slots__ = ("semantic_similarity", "structural_similarity", "structural_mapping")
    SEMANTIC_SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_MAPPING_FIELD_NUMBER: _ClassVar[int]
    semantic_similarity: float
    structural_similarity: float
    structural_mapping: _containers.RepeatedCompositeFieldContainer[RetrievedMapping]
    def __init__(self, semantic_similarity: _Optional[float] = ..., structural_similarity: _Optional[float] = ..., structural_mapping: _Optional[_Iterable[_Union[RetrievedMapping, _Mapping]]] = ...) -> None: ...
