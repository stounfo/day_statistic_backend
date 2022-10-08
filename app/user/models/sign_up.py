from uuid import uuid4

from aredis_om import JsonModel
from pydantic import BaseModel, EmailStr, Field

from app.common.models import TimestampedMixin
from app.common.security import create_access_code_factory
from app.common.types import AccessCodeStr, UsernameStr
from app.config import settings


class SignUpSessionBase(BaseModel):
    email: EmailStr


class SignUpEmailIn(SignUpSessionBase):
    pass


class SignUpEmailOut(SignUpEmailIn):
    sign_up_token: str


class SignUpAccessCodeIn(BaseModel):
    access_code: AccessCodeStr


class SignUpAccessCodeOut(SignUpSessionBase):
    pass


class SignUpUsernameIn(BaseModel):
    username: UsernameStr


class SignUpSessionDB(JsonModel, SignUpSessionBase, TimestampedMixin):
    verified: bool = False
    access_code: str = Field(
        default_factory=create_access_code_factory(
            settings.app.user_settings.access_code_len
        )
    )

    class Meta:
        primary_key_creator_cls = type(
            "UUIDPrimaryKey",
            (),
            {"create_pk": classmethod(lambda cls, *_, **__: str(uuid4()))},
        )
