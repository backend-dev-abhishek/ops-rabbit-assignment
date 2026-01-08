# ops-rabbit-assignment

A REST API for Log File Data Access and Analysis built with Python and FastAPI.

## Overview

This API provides endpoints to read, filter, and analyze log files stored in a specified directory. It efficiently parses log entries and provides statistical insights about the log data.

## Features

- **Log Reading & Parsing**: Read and parse log files with format `Timestamp\tLevel\Component\Message`
- **Filtering**: Filter logs by level, component, start time, and end time
- **Pagination**: Handle large log files with paginated results
- **Statistics**: Get aggregated statistics including counts by level and component
- **Error Handling**: Proper HTTP status codes and error messages for invalid requests

## API Endpoints

### GET /logs

Returns all log entries with optional filtering and pagination.

**Query Parameters:**
- `level` (optional): Filter by log level (e.g., ERROR, WARNING, INFO)
- `component` (optional): Filter by component name (e.g., UserAuth, Payment)
- `start_time` (optional): Filter logs after this timestamp (format: YYYY-MM-DD HH:MM:SS)
- `end_time` (optional): Filter logs before this timestamp (format: YYYY-MM-DD HH:MM:SS)
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 10)

**Response:**
```json
{
  "data": [
    {
      "id": "uuid-string",
      "timestamp": "2025-05-07 10:00:00",
      "level": "INFO",
      "component": "UserAuth",
      "message": "User 'john.doe' logged in successfully."
    }
  ],
  "pagination": {
    "total": 100,
    "skip": 0,
    "limit": 10,
    "has_more": true
  }
}
```

### GET /logs/stats

Returns statistics about the log data.

**Response:**
```json
{
  "total_logs": 100,
  "level_counts": {
    "INFO": 50,
    "WARNING": 30,
    "ERROR": 20
  },
  "component_counts": {
    "UserAuth": 40,
    "Payment": 35,
    "GeoIP": 25
  }
}
```

### GET /logs/{log_id}

Returns a specific log entry by its unique ID.

**Path Parameters:**
- `log_id`: The unique identifier of the log entry

**Response:**
```json
{
  "id": "uuid-string",
  "timestamp": "2025-05-07 10:00:00",
  "level": "INFO",
  "component": "UserAuth",
  "message": "User 'john.doe' logged in successfully."
}
```

**Error Response (404):**
```json
{
  "detail": "Log entry not found"
}
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ops-rabbit-assignment
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Open your browser or API client and navigate to:
```
http://localhost:8000/docs
```

This will open the automatic API documentation (Swagger UI) where you can test all endpoints.

## Log File Format

The API expects log files in the following format:
```
Timestamp\tLevel\Component\Message
```

Example:
```
2025-05-07 10:00:00	INFO	UserAuth	User 'john.doe' logged in successfully.
2025-05-07 10:00:15	WARNING	GeoIP	Could not resolve IP address '192.168.1.100'.
2025-05-07 10:00:20	ERROR	Payment	Transaction failed for user 'jane.doe'.
2025-05-07 10:00:25	INFO	UserAuth	User 'alice.smith' logged out.
```

Place your log files in the `logs/` directory. The API will automatically read all `.log` files from this directory.

## Project Structure

```
ops-rabbit-assignment/
├── app/
│   ├── __init__.py
│   ├── log_reader.py      # Log file parsing logic
│   ├── main.py            # FastAPI application and endpoints
│   └── models.py          # Pydantic models for request/response
├── logs/
│   └── info.log           # Sample log file
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Dependencies

- **fastapi**: Modern, fast web framework for building APIs
- **uvicorn**: ASGI server implementation
- **pydantic**: Data validation using Python type hints

## Example Requests

Get all INFO level logs:
```bash
curl "http://localhost:8000/logs?level=INFO"
```

Get logs from a specific component:
```bash
curl "http://localhost:8000/logs?component=UserAuth"
```

Get logs within a time range:
```bash
curl "http://localhost:8000/logs?start_time=2025-05-07%2010:00:00&end_time=2025-05-07%2010:00:30"
```

Get paginated results:
```bash
curl "http://localhost:8000/logs?skip=0&limit=5"
```

Get log statistics:
```bash
curl "http://localhost:8000/logs/stats"
```

Get a specific log by ID:
```bash
curl "http://localhost:8000/logs/{log_id}"
```

