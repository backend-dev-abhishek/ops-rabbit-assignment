from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from fastapi import Query

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

class Pagination(BaseModel):
    total: int
    skip: int
    limit: int
    has_more: bool

class PaginatedLogResponse(BaseModel):
    data: List[LogEntryResponse]
    pagination: Pagination