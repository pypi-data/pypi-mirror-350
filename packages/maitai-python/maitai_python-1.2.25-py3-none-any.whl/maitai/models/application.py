# codegen: frontend, sdk
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from maitai.models.config import Config


class ApplicationObjective(BaseModel):
    id: Optional[int] = 0
    date_created: Optional[float] = 0
    application_id: int
    objective_body: Dict[str, str] = Field(default_factory=dict)


class ApplicationAction(BaseModel):
    id: Optional[int] = -1
    action_type: str
    date_created: Optional[float] = 0
    application_id: int
    meta: Optional[Config] = None
    last_activity: Optional[int] = 0
    notifications_enabled: bool = False
    prompt: Optional[str] = None
    request_count: Optional[int] = 0
    intent_group_id: Optional[int] = -1


class Application(BaseModel):
    id: Optional[int] = -1
    date_created: Optional[float] = 0
    application_name: Optional[str] = None
    application_ref_name: Optional[str] = None
    company_id: int = 0
    application_objective: Optional[ApplicationObjective] = None
    state: Optional[str] = "ENABLED"
    meta: Optional[Config] = Field(default_factory=Config)
    action_types: List[ApplicationAction] = Field(default_factory=list)
    last_activity: Optional[int] = 0
    fault_notifications: Optional[bool] = False
    session_summaries: Optional[bool] = False


class ApplicationContext(BaseModel):
    id: Optional[int] = -1
    date_created: Optional[float] = 0
    application_id: Optional[int] = None
    context_body: Optional[Union[str, Dict[Any, Any]]] = None
    context_path: Optional[str] = None
    context_type: Optional[str] = "TEXT"
    reference: Optional[str] = None
    description: Optional[str] = None
