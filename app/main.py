import aioredis
import motor
from beanie import init_beanie
from fastapi import FastAPI

from app.config import Settings, settings
from app.user.models.sign_up import SignUpSessionDB
from app.user.models.user import UserDB
from app.user.routers import sign_up

app = FastAPI()

app.include_router(sign_up, prefix="/sign_up")


if settings.app.debug:

    @app.get("/settings", response_model=Settings, tags=["settings"])
    async def get_settings():
        return settings


@app.on_event("startup")
async def set_up_beanie():
    app.state.mongodb = motor.motor_asyncio.AsyncIOMotorClient(
        settings.mongodb.dsn
    )
    await init_beanie(
        database=app.state.mongodb.get_database(
            settings.mongodb.database_name
        ),
        document_models=[UserDB],
    )


@app.on_event("startup")
async def set_up_redis_om():
    app.state.redis = aioredis.Redis.from_url(settings.redis.dsn)
    SignUpSessionDB.Meta.database = (  # pyright: ignore[reportGeneralTypeIssues] # noqa: E501
        app.state.redis
    )
