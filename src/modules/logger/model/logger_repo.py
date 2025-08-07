from pymongo import ASCENDING
from datetime import datetime , timedelta, timezone
from ....config.db import dbClient

APP_LOGS_COLLECTION = "app_logs"

logger = dbClient[APP_LOGS_COLLECTION]



async def create_indexes():
    await logger.create_index([("userId", ASCENDING)])
    await logger.create_index([("eventType", ASCENDING)])
    await logger.create_index([("timestamp", ASCENDING)])


async def insert_log(data: dict):
    logDetails = await logger.insert_one(data)
    return str(logDetails.inserted_id)