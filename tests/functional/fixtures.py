import pytest
from pydantic import EmailStr

from app.common.types.types import UsernameStr
from app.user.models.sign_up import SignUpSessionDB
from app.user.models.user import UserDB


@pytest.fixture
async def some_user() -> UserDB:
    return await UserDB(
        email=EmailStr("test@mail.com"), username=UsernameStr("test")
    ).save()


@pytest.fixture
async def another_user() -> UserDB:
    return await UserDB(
        email=EmailStr("another_test@mail.com"),
        username=UsernameStr("another_test"),
    ).save()


@pytest.fixture
async def sign_up_session_waiting_for_access_code() -> SignUpSessionDB:
    return await SignUpSessionDB(email=EmailStr("test@mail.com")).save()


@pytest.fixture
async def sign_up_session_waiting_for_username(
    sign_up_session_waiting_for_access_code: SignUpSessionDB,
) -> SignUpSessionDB:
    sign_up_session_waiting_for_access_code.verified = True
    return await sign_up_session_waiting_for_access_code.save()
