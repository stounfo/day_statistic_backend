from datetime import timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, status

from app.common.email import send_email
from app.common.exceptions import (
    EmailAlreadyExistsException,
    EmailNotValidatedException,
    InvalidAccessCodeException,
    UsernameAlreadyExistsException,
)
from app.common.security import create_access_token
from app.config import settings

from ..dependencies import get_current_sign_up_session
from ..models.sign_up import (
    SignUpAccessCodeIn,
    SignUpAccessCodeOut,
    SignUpEmailIn,
    SignUpEmailOut,
    SignUpSessionDB,
    SignUpUsernameIn,
)
from ..models.user import UserDB, UserOut

sign_up = APIRouter(tags=["sign_up"])


@sign_up.post(
    "/email",
    response_model=SignUpEmailOut,
    status_code=status.HTTP_200_OK,
)
async def sign_up_email(
    data: SignUpEmailIn, background_tasks: BackgroundTasks
):
    email = data.email

    if await UserDB.find_one(UserDB.email == email):
        raise EmailAlreadyExistsException()

    sign_up_session = await SignUpSessionDB(email=email).save()
    await sign_up_session.expire(
        settings.app.user_settings.session_expire_time
    )

    background_tasks.add_task(
        send_email, email_to=email, access_code=sign_up_session.access_code
    )

    return SignUpEmailOut(
        email=email,
        sign_up_token=create_access_token(
            subject=sign_up_session.pk,
            expires_delta=timedelta(
                seconds=settings.app.user_settings.session_expire_time
            ),
        ),
    )


@sign_up.post(
    "/access_code",
    status_code=status.HTTP_200_OK,
    response_model=SignUpAccessCodeOut,
)
async def sign_up_access_code(
    data: SignUpAccessCodeIn,
    sign_up_session: SignUpSessionDB = Depends(get_current_sign_up_session),
):
    access_code = data.access_code
    if access_code != sign_up_session.access_code:
        raise InvalidAccessCodeException()

    sign_up_session.verified = True
    await sign_up_session.save()

    return SignUpAccessCodeOut(email=sign_up_session.email)


@sign_up.post(
    "/username",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up_username(
    data: SignUpUsernameIn,
    sign_up_session: SignUpSessionDB = Depends(get_current_sign_up_session),
):
    username = data.username
    if not sign_up_session.verified:
        raise EmailNotValidatedException()
    if await UserDB.find_one(UserDB.username == username):
        raise UsernameAlreadyExistsException()

    user = UserDB(
        id=sign_up_session.pk, email=sign_up_session.email, username=username
    )
    await user.save()
    await sign_up_session.delete(sign_up_session.pk)
    return UserOut(**user.dict())
