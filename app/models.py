from pydantic import BaseModel, validator, Extra
from datetime import datetime
from typing import List, Optional


class LogEntryResponse(BaseModel):
    id: str
    timestamp: str
    level: str
    component: str
    message: str

class LogStatsResponse(BaseModel):
    total_logs: int
    level_counts: dict
    component_counts: dict

class LogFilterParams(BaseModel):
    level: Optional[str] = None
    component: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    skip: int = 0
    limit: int = 10

    class Config:
        extra = Extra.forbid

    @validator("skip")
    def skip_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("skip must be greater than or equal to 0")
        return v

    @validator("limit")
    def limit_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("limit must be greater than or equal to 1")
        return v

    @validator("end_time")
    def end_time_must_be_after_start_time(cls, v, values):
        if "start_time" in values and values["start_time"] and v:
            if v < values["start_time"]:
                raise ValueError("end_time must be greater than or equal to start_time")
        return v

class Pagination(BaseModel):
    total: int
    skip: int
    limit: int
    has_more: bool

class PaginatedLogResponse(BaseModel):
    data: List[LogEntryResponse]
    pagination: Pagination