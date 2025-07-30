from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SimilarityMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIMILARITY_METHOD_UNSPECIFIED: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_COSINE: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_DYNAMAX_JACCARD: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_MAXPOOL_JACCARD: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_DYNAMAX_DICE: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_DYNAMAX_OTSUKA: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_WMD: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_EDIT: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_JACCARD: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_ANGULAR: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_MANHATTAN: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_EUCLIDEAN: _ClassVar[SimilarityMethod]
    SIMILARITY_METHOD_DOT: _ClassVar[SimilarityMethod]

class EmbeddingLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMBEDDING_LEVEL_UNSPECIFIED: _ClassVar[EmbeddingLevel]
    EMBEDDING_LEVEL_DOCUMENT: _ClassVar[EmbeddingLevel]
    EMBEDDING_LEVEL_TOKENS: _ClassVar[EmbeddingLevel]
    EMBEDDING_LEVEL_SENTENCES: _ClassVar[EmbeddingLevel]

class Pooling(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POOLING_UNSPECIFIED: _ClassVar[Pooling]
    POOLING_MEAN: _ClassVar[Pooling]
    POOLING_MAX: _ClassVar[Pooling]
    POOLING_MIN: _ClassVar[Pooling]
    POOLING_SUM: _ClassVar[Pooling]
    POOLING_FIRST: _ClassVar[Pooling]
    POOLING_LAST: _ClassVar[Pooling]
    POOLING_MEDIAN: _ClassVar[Pooling]
    POOLING_GMEAN: _ClassVar[Pooling]
    POOLING_HMEAN: _ClassVar[Pooling]

class EmbeddingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMBEDDING_TYPE_UNSPECIFIED: _ClassVar[EmbeddingType]
    EMBEDDING_TYPE_SPACY: _ClassVar[EmbeddingType]
    EMBEDDING_TYPE_TRANSFORMERS: _ClassVar[EmbeddingType]
    EMBEDDING_TYPE_SENTENCE_TRANSFORMERS: _ClassVar[EmbeddingType]
    EMBEDDING_TYPE_TENSORFLOW_HUB: _ClassVar[EmbeddingType]
    EMBEDDING_TYPE_OPENAI: _ClassVar[EmbeddingType]
    EMBEDDING_TYPE_OLLAMA: _ClassVar[EmbeddingType]
    EMBEDDING_TYPE_COHERE: _ClassVar[EmbeddingType]
    EMBEDDING_TYPE_VOYAGEAI: _ClassVar[EmbeddingType]
SIMILARITY_METHOD_UNSPECIFIED: SimilarityMethod
SIMILARITY_METHOD_COSINE: SimilarityMethod
SIMILARITY_METHOD_DYNAMAX_JACCARD: SimilarityMethod
SIMILARITY_METHOD_MAXPOOL_JACCARD: SimilarityMethod
SIMILARITY_METHOD_DYNAMAX_DICE: SimilarityMethod
SIMILARITY_METHOD_DYNAMAX_OTSUKA: SimilarityMethod
SIMILARITY_METHOD_WMD: SimilarityMethod
SIMILARITY_METHOD_EDIT: SimilarityMethod
SIMILARITY_METHOD_JACCARD: SimilarityMethod
SIMILARITY_METHOD_ANGULAR: SimilarityMethod
SIMILARITY_METHOD_MANHATTAN: SimilarityMethod
SIMILARITY_METHOD_EUCLIDEAN: SimilarityMethod
SIMILARITY_METHOD_DOT: SimilarityMethod
EMBEDDING_LEVEL_UNSPECIFIED: EmbeddingLevel
EMBEDDING_LEVEL_DOCUMENT: EmbeddingLevel
EMBEDDING_LEVEL_TOKENS: EmbeddingLevel
EMBEDDING_LEVEL_SENTENCES: EmbeddingLevel
POOLING_UNSPECIFIED: Pooling
POOLING_MEAN: Pooling
POOLING_MAX: Pooling
POOLING_MIN: Pooling
POOLING_SUM: Pooling
POOLING_FIRST: Pooling
POOLING_LAST: Pooling
POOLING_MEDIAN: Pooling
POOLING_GMEAN: Pooling
POOLING_HMEAN: Pooling
EMBEDDING_TYPE_UNSPECIFIED: EmbeddingType
EMBEDDING_TYPE_SPACY: EmbeddingType
EMBEDDING_TYPE_TRANSFORMERS: EmbeddingType
EMBEDDING_TYPE_SENTENCE_TRANSFORMERS: EmbeddingType
EMBEDDING_TYPE_TENSORFLOW_HUB: EmbeddingType
EMBEDDING_TYPE_OPENAI: EmbeddingType
EMBEDDING_TYPE_OLLAMA: EmbeddingType
EMBEDDING_TYPE_COHERE: EmbeddingType
EMBEDDING_TYPE_VOYAGEAI: EmbeddingType

class NlpConfig(_message.Message):
    __slots__ = ("language", "spacy_model", "embedding_models", "similarity_method")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SPACY_MODEL_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_MODELS_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_METHOD_FIELD_NUMBER: _ClassVar[int]
    language: str
    spacy_model: str
    embedding_models: _containers.RepeatedCompositeFieldContainer[EmbeddingModel]
    similarity_method: SimilarityMethod
    def __init__(self, language: _Optional[str] = ..., spacy_model: _Optional[str] = ..., embedding_models: _Optional[_Iterable[_Union[EmbeddingModel, _Mapping]]] = ..., similarity_method: _Optional[_Union[SimilarityMethod, str]] = ...) -> None: ...

class SimilaritiesRequest(_message.Message):
    __slots__ = ("config", "text_tuples", "extras")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    TEXT_TUPLES_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    config: NlpConfig
    text_tuples: _containers.RepeatedCompositeFieldContainer[TextTuple]
    extras: _struct_pb2.Struct
    def __init__(self, config: _Optional[_Union[NlpConfig, _Mapping]] = ..., text_tuples: _Optional[_Iterable[_Union[TextTuple, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SimilaritiesResponse(_message.Message):
    __slots__ = ("similarities", "extras")
    SIMILARITIES_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    similarities: _containers.RepeatedScalarFieldContainer[float]
    extras: _struct_pb2.Struct
    def __init__(self, similarities: _Optional[_Iterable[float]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class TextTuple(_message.Message):
    __slots__ = ("text1", "text2")
    TEXT1_FIELD_NUMBER: _ClassVar[int]
    TEXT2_FIELD_NUMBER: _ClassVar[int]
    text1: str
    text2: str
    def __init__(self, text1: _Optional[str] = ..., text2: _Optional[str] = ...) -> None: ...

class Strings(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class DocBinRequest(_message.Message):
    __slots__ = ("config", "texts", "attributes", "enabled_pipes", "disabled_pipes", "embedding_levels", "extras")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    TEXTS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    ENABLED_PIPES_FIELD_NUMBER: _ClassVar[int]
    DISABLED_PIPES_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_LEVELS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    config: NlpConfig
    texts: _containers.RepeatedScalarFieldContainer[str]
    attributes: Strings
    enabled_pipes: Strings
    disabled_pipes: Strings
    embedding_levels: _containers.RepeatedScalarFieldContainer[EmbeddingLevel]
    extras: _struct_pb2.Struct
    def __init__(self, config: _Optional[_Union[NlpConfig, _Mapping]] = ..., texts: _Optional[_Iterable[str]] = ..., attributes: _Optional[_Union[Strings, _Mapping]] = ..., enabled_pipes: _Optional[_Union[Strings, _Mapping]] = ..., disabled_pipes: _Optional[_Union[Strings, _Mapping]] = ..., embedding_levels: _Optional[_Iterable[_Union[EmbeddingLevel, str]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class DocBinResponse(_message.Message):
    __slots__ = ("docbin", "extras")
    DOCBIN_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    docbin: bytes
    extras: _struct_pb2.Struct
    def __init__(self, docbin: _Optional[bytes] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class VectorsRequest(_message.Message):
    __slots__ = ("config", "texts", "embedding_levels", "extras")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    TEXTS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_LEVELS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    config: NlpConfig
    texts: _containers.RepeatedScalarFieldContainer[str]
    embedding_levels: _containers.RepeatedScalarFieldContainer[EmbeddingLevel]
    extras: _struct_pb2.Struct
    def __init__(self, config: _Optional[_Union[NlpConfig, _Mapping]] = ..., texts: _Optional[_Iterable[str]] = ..., embedding_levels: _Optional[_Iterable[_Union[EmbeddingLevel, str]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class VectorsResponse(_message.Message):
    __slots__ = ("vectors", "extras")
    VECTORS_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    vectors: _containers.RepeatedCompositeFieldContainer[VectorResponse]
    extras: _struct_pb2.Struct
    def __init__(self, vectors: _Optional[_Iterable[_Union[VectorResponse, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class VectorResponse(_message.Message):
    __slots__ = ("document", "tokens", "sentences", "extras")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    SENTENCES_FIELD_NUMBER: _ClassVar[int]
    EXTRAS_FIELD_NUMBER: _ClassVar[int]
    document: Vector
    tokens: _containers.RepeatedCompositeFieldContainer[Vector]
    sentences: _containers.RepeatedCompositeFieldContainer[Vector]
    extras: _struct_pb2.Struct
    def __init__(self, document: _Optional[_Union[Vector, _Mapping]] = ..., tokens: _Optional[_Iterable[_Union[Vector, _Mapping]]] = ..., sentences: _Optional[_Iterable[_Union[Vector, _Mapping]]] = ..., extras: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Vector(_message.Message):
    __slots__ = ("vector",)
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    vector: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, vector: _Optional[_Iterable[float]] = ...) -> None: ...

class EmbeddingModel(_message.Message):
    __slots__ = ("model_type", "model_name", "pooling_type", "pmean")
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    POOLING_TYPE_FIELD_NUMBER: _ClassVar[int]
    PMEAN_FIELD_NUMBER: _ClassVar[int]
    model_type: EmbeddingType
    model_name: str
    pooling_type: Pooling
    pmean: float
    def __init__(self, model_type: _Optional[_Union[EmbeddingType, str]] = ..., model_name: _Optional[str] = ..., pooling_type: _Optional[_Union[Pooling, str]] = ..., pmean: _Optional[float] = ...) -> None: ...
