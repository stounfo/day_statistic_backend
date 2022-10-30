from uuid import uuid4

from aredis_om import JsonModel
from pydantic import BaseModel, EmailStr, Field

from app.common.models import TimestampedMixin
from app.common.types import AccessCodeStr, UsernameStr


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
    access_code: AccessCodeStr = Field(default_factory=AccessCodeStr.random)

    class Meta:
        primary_key_creator_cls = type(
            "UUIDPrimaryKey",
            (),
            {"create_pk": classmethod(lambda cls, *_, **__: str(uuid4()))},
        )
