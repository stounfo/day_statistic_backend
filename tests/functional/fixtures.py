import pytest
from pydantic import EmailStr

from app.user.models.sign_up import SignUpSessionDB
from app.user.models.user import UserDB


@pytest.fixture
async def some_user() -> UserDB:
    return await UserDB(
        email=EmailStr("test@mail.com"), username="test"
    ).save()


@pytest.fixture
async def another_user() -> UserDB:
    return await UserDB(
        email=EmailStr("another_test@mail.com"), username="another_test"
    ).save()


@pytest.fixture
async def sign_up_session_get_email() -> SignUpSessionDB:
    return await SignUpSessionDB(email=EmailStr("test@mail.com")).save()


@pytest.fixture
async def sign_up_session_get_access_code(
    sign_up_session_get_email: SignUpSessionDB,
) -> SignUpSessionDB:
    sign_up_session_get_email.verified = True
    return await sign_up_session_get_email.save()
