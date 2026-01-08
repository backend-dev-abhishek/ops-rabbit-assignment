from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
from datetime import datetime
from app.models import LogEntryResponse, LogStatsResponse, LogFilterParams
from app.log_reader import get_all_logs
from collections import Counter

app = FastAPI()

LOG_DIRECTORY = "./logs" 

logs = get_all_logs(LOG_DIRECTORY)

# for i in logs:
#     print(i)
# log_dict: Dict[str, LogEntryResponse] = {log.id: log for log in logs}

log_dict: Dict[str, dict] = {log.id: log.to_dict() for log in logs}

@app.get("/logs", response_model=List[LogEntryResponse])
def get_logs(params: LogFilterParams = Query(...)):
    def matches_filters(log) -> bool:
        if params.level and log.level != params.level:
            return False
        if params.component and log.component != params.component:
            return False
        if params.start_time:
            log_time = datetime.strptime(log.timestamp, "%Y-%m-%d %H:%M:%S")
            if log_time < params.start_time:
                return False
        if params.end_time:
            log_time = datetime.strptime(log.timestamp, "%Y-%m-%d %H:%M:%S")
            if log_time > params.end_time:
                return False
        return True
    return [log_dict[log.id] for log in logs if matches_filters(log)]

@app.get("/logs/stats", response_model=LogStatsResponse)
def get_log_stats():
    level_counts = Counter(log.level for log in logs)
    component_counts = Counter(log.component for log in logs)
    
    return LogStatsResponse(
        total_logs=len(logs),
        level_counts=dict(level_counts),
        component_counts=dict(component_counts)
    )

@app.get("/logs/{log_id}", response_model=LogEntryResponse)
def get_log_by_id(log_id: str):
    if log_id not in log_dict:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return log_dict[log_id]

