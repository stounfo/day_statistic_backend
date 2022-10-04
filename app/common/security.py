import secrets
from datetime import datetime, timedelta
from typing import Callable
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app.common.models import TokenPayload


def create_access_token(subject: str, expires_delta: timedelta) -> str:
    to_encode = TokenPayload(
        sub=UUID(subject), exp=datetime.now() + expires_delta
    )
    return str(jsonable_encoder(to_encode.dict()))


def create_access_code_factory(length: int) -> Callable[[], str]:
    def wrapped() -> str:
        return "".join([str(secrets.choice(range(10))) for i in range(length)])

    return wrapped
