from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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