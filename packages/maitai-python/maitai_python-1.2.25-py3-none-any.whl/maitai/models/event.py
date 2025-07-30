# codegen: sdk
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: Optional[int] = -1
    date_created: Optional[float] = 0
    event_type: str
    event_key: str
    event_data: str
    source_ips: Union[List[str], str] = Field(default_factory=list)
