# global_service

A Python package for global logging, step-wise logging, and Oracle DB activity logging, with robust log delivery and local fallback.

## Features
- Centralized logging to a global service (HTTP endpoint)
- Step-wise logger for tracking process steps
- Oracle DB logging for web activity
- Local fallback for failed log delivery
- Fully dynamic configuration via code or environment variables

## Installation

```powershell
pip install global_service
```

## Usage

```python
from global_service import config, build_global_log_payload, send_log_to_global_service, StepLogger, save_step_logs_to_oracle

# Configure dynamically (recommended)
config.configure(
    GLOBAL_LOG_URL="http://your-log-server:8000/web_logs",
    APP_CODE="MY-APP-CODE",
    ORACLE_DB_HOST="dbhost",
    ORACLE_DB_PORT=1521,
    ORACLE_DB_SERVICE="ORCLPDB",
    ORACLE_USER="user",
    ORACLE_PASS="pass"
)

# Example: Send a log
payload = build_global_log_payload(request)
send_log_to_global_service(payload)

# Example: Step logger
step_logger = StepLogger()
step_logger.log("Step 1: Started")
step_logger.log("Step 2: Processing")
# ...
save_step_logs_to_oracle(payload, step_logger, request_body, response_body)
```

## Environment Variables (optional)
- `GLOBAL_LOG_URL`
- `APP_CODE`
- `ORACLE_DB_HOST`, `ORACLE_DB_PORT`, `ORACLE_DB_SERVICE`, `ORACLE_DB_USER`, `ORACLE_DB_PASS`

## License
MIT
