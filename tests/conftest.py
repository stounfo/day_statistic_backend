from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.config import MongoDB, Redis, settings
from app.main import app

settings.mongodb = MongoDB(
    **{
        **settings.mongodb.dict(),
        "database_name": f"test_{settings.mongodb.database_name}",
    }
)

settings.redis = Redis(
    **{
        **settings.redis.dict(),
        "database_name": "15",
    }
)
pytest_plugins = ("anyio", "tests.functional.fixtures")


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=app, base_url="http://test"
    ) as c, LifespanManager(app):
        yield c


@pytest.fixture(scope="function", autouse=True)
async def cleanup_redis():
    yield
    await app.state.redis.flushdb()


@pytest.fixture(scope="function", autouse=True)
async def cleanup_mongodb():
    yield
    await app.state.mongodb.drop_database(settings.mongodb.database_name)
