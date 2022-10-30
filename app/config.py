# https://pydantic-docs.helpmanual.io/visual_studio_code/#basesettings-and-ignoring-pylancepyright-errors
# pyright: reportGeneralTypeIssues=false
from typing import Any, Dict, TypeAlias

from pydantic import BaseSettings, Field, MongoDsn, RedisDsn, root_validator

HostStr: TypeAlias = str
PortStr: TypeAlias = str
SecondInt: TypeAlias = int


class User(BaseSettings):
    session_expire_time: SecondInt = Field(
        env="SING_UP_SESSION_EXPIRE_TIME", gt=0
    )

    class Config:
        env_file = "./etc/envs/app.user.env", "../etc/envs/app.user.env"


class App(BaseSettings):
    user_settings: User = User()
    debug: bool = Field(env="APP_DEBUG")

    class Config:
        env_file = "./etc/envs/app.env", "../etc/envs/app.env"


class MongoDB(BaseSettings):
    host: HostStr = Field(env="MONGO_HOST")
    port: PortStr = Field(env="MONGO_PORT")
    database_name: str = Field(env="MONGO_DATABASE_NAME")
    username: str = Field(env="MONGO_INITDB_ROOT_USERNAME")
    password: str = Field(env="MONGO_INITDB_ROOT_PASSWORD")
    dsn: MongoDsn

    @root_validator(pre=True)
    def assemble_dsn(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["dsn"] = MongoDsn.build(
            scheme="mongodb",
            host=values["host"],
            port=values["port"],
            user=values["username"],
            password=values["password"],
        )
        return values

    class Config:
        env_file = "./etc/envs/mongodb.env", "../etc/envs/mongodb.env"


class Redis(BaseSettings):
    host: HostStr = Field(env="REDIS_HOST")
    port: PortStr = Field(env="REDIS_PORT")
    database_name: str = Field(env="DATABASE_NAME")
    dsn: RedisDsn

    @root_validator(pre=True)
    def assemble_dsn(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["dsn"] = RedisDsn.build(
            scheme="redis",
            host=values["host"],
            port=values["port"],
            path=f"/{values['database_name']}",
        )
        return values

    class Config:
        env_file = "./etc/envs/redis.env", "../etc/envs/redis.env"


class Settings(BaseSettings):
    app: App = App()
    mongodb: MongoDB = MongoDB()
    redis: Redis = Redis()

    class Config:
        validate_assignment = True


settings = Settings()
