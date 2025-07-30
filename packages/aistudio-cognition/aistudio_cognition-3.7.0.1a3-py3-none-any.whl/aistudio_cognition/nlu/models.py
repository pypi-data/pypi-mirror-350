from dataclasses import dataclass
from typing import Optional, Union

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Intent:
    name: str
    confidence: float


@dataclass_json
@dataclass
class Category:
    level: int
    intents: list[Intent]


@dataclass_json
@dataclass
class Entity:
    name: str
    confidence: int
    value: str


@dataclass_json
@dataclass
class Group:
    operation: str
    group: list[Union[Entity, "Group"]]


@dataclass_json
@dataclass
class Rules:
    name: str
    priority: int
    categories: Optional[list[Category]] = None
    regex: Optional[str] = None
    entities: Union[Entity, Group, None] = None
