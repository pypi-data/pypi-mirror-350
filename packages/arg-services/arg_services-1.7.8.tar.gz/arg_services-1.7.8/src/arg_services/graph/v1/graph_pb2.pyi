from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Support(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUPPORT_DEFAULT: _ClassVar[Support]
    SUPPORT_POSITION_TO_KNOW: _ClassVar[Support]
    SUPPORT_EXPERT_OPINION: _ClassVar[Support]
    SUPPORT_WITNESS_TESTIMONY: _ClassVar[Support]
    SUPPORT_POPULAR_OPINION: _ClassVar[Support]
    SUPPORT_POPULAR_PRACTICE: _ClassVar[Support]
    SUPPORT_EXAMPLE: _ClassVar[Support]
    SUPPORT_ANALOGY: _ClassVar[Support]
    SUPPORT_PRACTICAL_REASONING_FROM_ANALOGY: _ClassVar[Support]
    SUPPORT_COMPOSITION: _ClassVar[Support]
    SUPPORT_DIVISION: _ClassVar[Support]
    SUPPORT_OPPOSITIONS: _ClassVar[Support]
    SUPPORT_RHETORICAL_OPPOSITIONS: _ClassVar[Support]
    SUPPORT_ALTERNATIVES: _ClassVar[Support]
    SUPPORT_VERBAL_CLASSIFICATION: _ClassVar[Support]
    SUPPORT_VERBAL_CLASSIFICATION_DEFINITION: _ClassVar[Support]
    SUPPORT_VERBAL_CLASSIFICATION_VAGUENESS: _ClassVar[Support]
    SUPPORT_VERBAL_CLASSIFICATION_ARBITRARINESS: _ClassVar[Support]
    SUPPORT_INTERACTION_OF_ACT_AND_PERSON: _ClassVar[Support]
    SUPPORT_VALUES: _ClassVar[Support]
    SUPPORT_POSITIVE_VALUES: _ClassVar[Support]
    SUPPORT_NEGATIVE_VALUES: _ClassVar[Support]
    SUPPORT_SACRIFICE: _ClassVar[Support]
    SUPPORT_THE_GROUP_AND_ITS_MEMBERS: _ClassVar[Support]
    SUPPORT_PRACTICAL_REASONING: _ClassVar[Support]
    SUPPORT_TWO_PERSON_PRACTICAL_REASONING: _ClassVar[Support]
    SUPPORT_WASTE: _ClassVar[Support]
    SUPPORT_SUNK_COSTS: _ClassVar[Support]
    SUPPORT_IGNORANCE: _ClassVar[Support]
    SUPPORT_EPISTEMIC_IGNORANCE: _ClassVar[Support]
    SUPPORT_CAUSE_TO_EFFECT: _ClassVar[Support]
    SUPPORT_CORRELATION_TO_CAUSE: _ClassVar[Support]
    SUPPORT_SIGN: _ClassVar[Support]
    SUPPORT_ABDUCTIVE: _ClassVar[Support]
    SUPPORT_EVIDENCE_TO_HYPOTHESIS: _ClassVar[Support]
    SUPPORT_CONSEQUENCES: _ClassVar[Support]
    SUPPORT_POSITIVE_CONSEQUENCES: _ClassVar[Support]
    SUPPORT_NEGATIVE_CONSEQUENCES: _ClassVar[Support]
    SUPPORT_PRAGMATIC_ALTERNATIVES: _ClassVar[Support]
    SUPPORT_THREAT: _ClassVar[Support]
    SUPPORT_FEAR_APPEAL: _ClassVar[Support]
    SUPPORT_DANGER_APPEAL: _ClassVar[Support]
    SUPPORT_NEED_FOR_HELP: _ClassVar[Support]
    SUPPORT_DISTRESS: _ClassVar[Support]
    SUPPORT_COMMITMENT: _ClassVar[Support]
    SUPPORT_ETHOTIC: _ClassVar[Support]
    SUPPORT_GENERIC_AD_HOMINEM: _ClassVar[Support]
    SUPPORT_PRAGMATIC_INCONSISTENCY: _ClassVar[Support]
    SUPPORT_INCONSISTENT_COMMITMENT: _ClassVar[Support]
    SUPPORT_CIRCUMSTANTIAL_AD_HOMINEM: _ClassVar[Support]
    SUPPORT_BIAS: _ClassVar[Support]
    SUPPORT_BIAS_AD_HOMINEM: _ClassVar[Support]
    SUPPORT_GRADUALISM: _ClassVar[Support]
    SUPPORT_SLIPPERY_SLOPE: _ClassVar[Support]
    SUPPORT_PRECEDENT_SLIPPERY_SLOPE: _ClassVar[Support]
    SUPPORT_SORITES_SLIPPERY_SLOPE: _ClassVar[Support]
    SUPPORT_VERBAL_SLIPPERY_SLOPE: _ClassVar[Support]
    SUPPORT_FULL_SLIPPERY_SLOPE: _ClassVar[Support]
    SUPPORT_CONSTITUTIVE_RULE_CLAIMS: _ClassVar[Support]
    SUPPORT_RULES: _ClassVar[Support]
    SUPPORT_EXCEPTIONAL_CASE: _ClassVar[Support]
    SUPPORT_PRECEDENT: _ClassVar[Support]
    SUPPORT_PLEA_FOR_EXCUSE: _ClassVar[Support]
    SUPPORT_PERCEPTION: _ClassVar[Support]
    SUPPORT_MEMORY: _ClassVar[Support]

class Attack(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ATTACK_DEFAULT: _ClassVar[Attack]

class Preference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PREFERENCE_DEFAULT: _ClassVar[Preference]

class Rephrase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPHRASE_DEFAULT: _ClassVar[Rephrase]
SUPPORT_DEFAULT: Support
SUPPORT_POSITION_TO_KNOW: Support
SUPPORT_EXPERT_OPINION: Support
SUPPORT_WITNESS_TESTIMONY: Support
SUPPORT_POPULAR_OPINION: Support
SUPPORT_POPULAR_PRACTICE: Support
SUPPORT_EXAMPLE: Support
SUPPORT_ANALOGY: Support
SUPPORT_PRACTICAL_REASONING_FROM_ANALOGY: Support
SUPPORT_COMPOSITION: Support
SUPPORT_DIVISION: Support
SUPPORT_OPPOSITIONS: Support
SUPPORT_RHETORICAL_OPPOSITIONS: Support
SUPPORT_ALTERNATIVES: Support
SUPPORT_VERBAL_CLASSIFICATION: Support
SUPPORT_VERBAL_CLASSIFICATION_DEFINITION: Support
SUPPORT_VERBAL_CLASSIFICATION_VAGUENESS: Support
SUPPORT_VERBAL_CLASSIFICATION_ARBITRARINESS: Support
SUPPORT_INTERACTION_OF_ACT_AND_PERSON: Support
SUPPORT_VALUES: Support
SUPPORT_POSITIVE_VALUES: Support
SUPPORT_NEGATIVE_VALUES: Support
SUPPORT_SACRIFICE: Support
SUPPORT_THE_GROUP_AND_ITS_MEMBERS: Support
SUPPORT_PRACTICAL_REASONING: Support
SUPPORT_TWO_PERSON_PRACTICAL_REASONING: Support
SUPPORT_WASTE: Support
SUPPORT_SUNK_COSTS: Support
SUPPORT_IGNORANCE: Support
SUPPORT_EPISTEMIC_IGNORANCE: Support
SUPPORT_CAUSE_TO_EFFECT: Support
SUPPORT_CORRELATION_TO_CAUSE: Support
SUPPORT_SIGN: Support
SUPPORT_ABDUCTIVE: Support
SUPPORT_EVIDENCE_TO_HYPOTHESIS: Support
SUPPORT_CONSEQUENCES: Support
SUPPORT_POSITIVE_CONSEQUENCES: Support
SUPPORT_NEGATIVE_CONSEQUENCES: Support
SUPPORT_PRAGMATIC_ALTERNATIVES: Support
SUPPORT_THREAT: Support
SUPPORT_FEAR_APPEAL: Support
SUPPORT_DANGER_APPEAL: Support
SUPPORT_NEED_FOR_HELP: Support
SUPPORT_DISTRESS: Support
SUPPORT_COMMITMENT: Support
SUPPORT_ETHOTIC: Support
SUPPORT_GENERIC_AD_HOMINEM: Support
SUPPORT_PRAGMATIC_INCONSISTENCY: Support
SUPPORT_INCONSISTENT_COMMITMENT: Support
SUPPORT_CIRCUMSTANTIAL_AD_HOMINEM: Support
SUPPORT_BIAS: Support
SUPPORT_BIAS_AD_HOMINEM: Support
SUPPORT_GRADUALISM: Support
SUPPORT_SLIPPERY_SLOPE: Support
SUPPORT_PRECEDENT_SLIPPERY_SLOPE: Support
SUPPORT_SORITES_SLIPPERY_SLOPE: Support
SUPPORT_VERBAL_SLIPPERY_SLOPE: Support
SUPPORT_FULL_SLIPPERY_SLOPE: Support
SUPPORT_CONSTITUTIVE_RULE_CLAIMS: Support
SUPPORT_RULES: Support
SUPPORT_EXCEPTIONAL_CASE: Support
SUPPORT_PRECEDENT: Support
SUPPORT_PLEA_FOR_EXCUSE: Support
SUPPORT_PERCEPTION: Support
SUPPORT_MEMORY: Support
ATTACK_DEFAULT: Attack
PREFERENCE_DEFAULT: Preference
REPHRASE_DEFAULT: Rephrase

class Graph(_message.Message):
    __slots__ = ("nodes", "edges", "resources", "participants", "analysts", "major_claim", "schema_version", "library_version", "metadata", "userdata")
    class NodesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Node
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Node, _Mapping]] = ...) -> None: ...
    class EdgesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Edge
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Edge, _Mapping]] = ...) -> None: ...
    class ResourcesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Resource
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Resource, _Mapping]] = ...) -> None: ...
    class ParticipantsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Participant
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Participant, _Mapping]] = ...) -> None: ...
    class AnalystsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Analyst
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Analyst, _Mapping]] = ...) -> None: ...
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    ANALYSTS_FIELD_NUMBER: _ClassVar[int]
    MAJOR_CLAIM_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.MessageMap[str, Node]
    edges: _containers.MessageMap[str, Edge]
    resources: _containers.MessageMap[str, Resource]
    participants: _containers.MessageMap[str, Participant]
    analysts: _containers.MessageMap[str, Analyst]
    major_claim: str
    schema_version: int
    library_version: str
    metadata: Metadata
    userdata: _struct_pb2.Struct
    def __init__(self, nodes: _Optional[_Mapping[str, Node]] = ..., edges: _Optional[_Mapping[str, Edge]] = ..., resources: _Optional[_Mapping[str, Resource]] = ..., participants: _Optional[_Mapping[str, Participant]] = ..., analysts: _Optional[_Mapping[str, Analyst]] = ..., major_claim: _Optional[str] = ..., schema_version: _Optional[int] = ..., library_version: _Optional[str] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ..., userdata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ("created", "updated")
    CREATED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    updated: _timestamp_pb2.Timestamp
    def __init__(self, created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Resource(_message.Message):
    __slots__ = ("text", "title", "source", "timestamp", "metadata", "userdata")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    text: str
    title: str
    source: str
    timestamp: _timestamp_pb2.Timestamp
    metadata: Metadata
    userdata: _struct_pb2.Struct
    def __init__(self, text: _Optional[str] = ..., title: _Optional[str] = ..., source: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ..., userdata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Participant(_message.Message):
    __slots__ = ("name", "username", "email", "url", "location", "description", "metadata", "userdata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    username: str
    email: str
    url: str
    location: str
    description: str
    metadata: Metadata
    userdata: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., url: _Optional[str] = ..., location: _Optional[str] = ..., description: _Optional[str] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ..., userdata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Analyst(_message.Message):
    __slots__ = ("name", "email", "userdata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    userdata: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., userdata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Edge(_message.Message):
    __slots__ = ("source", "target", "metadata", "userdata")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    source: str
    target: str
    metadata: Metadata
    userdata: _struct_pb2.Struct
    def __init__(self, source: _Optional[str] = ..., target: _Optional[str] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ..., userdata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ("atom", "scheme", "metadata", "userdata")
    ATOM_FIELD_NUMBER: _ClassVar[int]
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    atom: Atom
    scheme: Scheme
    metadata: Metadata
    userdata: _struct_pb2.Struct
    def __init__(self, atom: _Optional[_Union[Atom, _Mapping]] = ..., scheme: _Optional[_Union[Scheme, _Mapping]] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ..., userdata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Atom(_message.Message):
    __slots__ = ("text", "reference", "participant")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    text: str
    reference: Reference
    participant: str
    def __init__(self, text: _Optional[str] = ..., reference: _Optional[_Union[Reference, _Mapping]] = ..., participant: _Optional[str] = ...) -> None: ...

class Reference(_message.Message):
    __slots__ = ("resource", "offset", "text")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    resource: str
    offset: int
    text: str
    def __init__(self, resource: _Optional[str] = ..., offset: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class Scheme(_message.Message):
    __slots__ = ("support", "attack", "preference", "rephrase", "premise_descriptors")
    SUPPORT_FIELD_NUMBER: _ClassVar[int]
    ATTACK_FIELD_NUMBER: _ClassVar[int]
    PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    REPHRASE_FIELD_NUMBER: _ClassVar[int]
    PREMISE_DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    support: Support
    attack: Attack
    preference: Preference
    rephrase: Rephrase
    premise_descriptors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, support: _Optional[_Union[Support, str]] = ..., attack: _Optional[_Union[Attack, str]] = ..., preference: _Optional[_Union[Preference, str]] = ..., rephrase: _Optional[_Union[Rephrase, str]] = ..., premise_descriptors: _Optional[_Iterable[str]] = ...) -> None: ...
