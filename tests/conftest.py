import pytest_asyncio
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv('.env.testing')
load_dotenv(env_file)

from src.core.database import BaseModel, db_helper
from src.core.config import settings, Environment

@pytest_asyncio.fixture(scope='session', autouse=True)
async def load_env() -> None:
    if settings.app.environment != Environment.TEST:
        raise Exception('Wrong environment')

@pytest_asyncio.fixture(scope="session", autouse=True)
async def migrate_test_db() -> None:
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    yield "Test database"
