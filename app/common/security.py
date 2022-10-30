from datetime import datetime, timedelta
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app.common.models import TokenPayload


def create_access_token(subject: str, expires_delta: timedelta) -> str:
    to_encode = TokenPayload(
        sub=UUID(subject), exp=datetime.now() + expires_delta
    )
    return str(jsonable_encoder(to_encode.dict()))
