import os
import uuid
from typing import List

class LogEntry:
    def __init__(self, timestamp: str, level: str, component: str, message: str):
        self.timestamp = timestamp
        self.level = level
        self.component = component
        self.message = message
        self.id = str(uuid.uuid4())

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "level": self.level,
            "component": self.component,
            "message": self.message
        }

def get_all_logs(directory: str) -> List[LogEntry]:
    logs = []
    for filename in os.listdir(directory):
        # file_path = os.path.join(directory, "info.log")
        if filename.endswith(".log"):
            file_path = os.path.join(directory, filename)
            logs.extend(read_log_file(file_path))
    return logs

def read_log_file(file_path: str) -> List[LogEntry]:
    logs = []
    with open(file_path, 'r') as file_data:
        for line in file_data:
            parts = line.strip().split("\\t")
            if len(parts) == 4:
                timestamp, level, component, message = parts
                log_entry = LogEntry(timestamp, level, component, message)
                logs.append(log_entry)
    return logs