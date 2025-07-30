# codegen: sdk
from humps import camelize
from pydantic import AliasGenerator, BaseModel, ConfigDict


class RequestTimingMetric(BaseModel):
    time_request_start: float
    time_pre_request: float = 0
    time_first_chunk: float = 0
    time_request_end: float = 0
    request_id: str = ""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=camelize,
        ),
        populate_by_name=True,
    )
