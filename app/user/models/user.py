from uuid import UUID, uuid4

from beanie import Document
from pydantic import BaseModel, EmailStr, Field

from app.common.models import TimestampedMixin
from app.common.types import UsernameStr


class UserBase(BaseModel, TimestampedMixin):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    username: UsernameStr


class UserOut(UserBase):
    pass


class UserDB(UserBase, Document):
    pass
