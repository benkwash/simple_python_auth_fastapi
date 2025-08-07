from datetime import datetime, timezone
from ..model.logger_repo import insert_log

async def log_event(data: dict):
    log = {
        **data,
        "timestamp": datetime.now(timezone.utc)
    }
    print(log)
    
    await insert_log(log)