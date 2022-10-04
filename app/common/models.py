from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TimestampedMixin:
    created_at: datetime = Field(default_factory=datetime.now)


class TokenPayload(BaseModel):
    sub: UUID
    exp: datetime = Field(default_factory=datetime.now)
