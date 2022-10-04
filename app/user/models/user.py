from uuid import UUID, uuid4

from beanie import Document
from pydantic import BaseModel, EmailStr, Field

from app.common.fields import UsernameStr
from app.common.models import TimestampedMixin


class UserBase(BaseModel, TimestampedMixin):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    username: UsernameStr


class UserOut(UserBase):
    pass


class UserDB(UserBase, Document):
    pass
