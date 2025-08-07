from ..modules.users.model.user_repo import create_indexes as create_user_indexes
from ..modules.logger.model.logger_repo import create_indexes as create_logger_indexes

async def create_indexes():
    await create_user_indexes()
    await create_logger_indexes()