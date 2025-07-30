# codegen: frontend, sdk
from enum import IntEnum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class SeverityLevel(IntEnum):
    UNRECOGNIZED = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4


class SentinelExample(BaseModel):
    example_type: str
    example_body: str


class DirectiveBody(BaseModel):
    main: Optional[str] = None
    override: Optional[str] = None


class SentinelDirective(BaseModel):
    id: Optional[int] = -1
    sentinel_id: Optional[int] = None
    date_created: Optional[float] = 0
    directive_body: DirectiveBody
    examples: List[SentinelExample] = Field(default_factory=list)


class SentinelQa(BaseModel):
    question: str
    answer: str


class Sentinel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    sentinel_name: str
    action_types: List[str] = None
    severity: Union[SeverityLevel, int]
    meta: Dict[str, Any] = Field(default_factory=dict)
    qa: List[SentinelQa] = Field(default_factory=list)

    id: Optional[int] = -1
    application_id: Optional[int] = None
    sentinel_name: str
    date_created: Optional[float] = 0
    sentinel_directive: Optional[SentinelDirective] = None
    state: Optional[str] = None
    sentinel_generation_id: Optional[int] = None
    intent_group_id: Optional[int] = None
    sentinel_type: Optional[str] = None


class SentinelGeneration(BaseModel):
    id: Optional[int] = -1
    date_created: Optional[float] = 0
    company_id: int = 0
    application_id: Optional[int] = None
    application_action_id: Optional[int] = None
    base_prompt: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    generation_successful: bool = False
    intent_group_id: Optional[int] = None
    sentinel_type: Optional[str] = None
