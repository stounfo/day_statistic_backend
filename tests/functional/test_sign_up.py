from datetime import timedelta
from typing import Dict

import pytest
from fastapi import status
from httpx import AsyncClient

from app.common.security import create_access_token
from app.config import settings
from app.main import app
from app.user.models.sign_up import SignUpSessionDB
from app.user.models.user import UserDB


@pytest.mark.anyio
async def test_sign_up_email_success(client: AsyncClient):
    payload = {"email": "test@mail.com"}
    response = await client.post(
        app.url_path_for("sign_up_email"), json=payload
    )
    assert response.status_code == status.HTTP_200_OK
    response_body = response.json()
    assert response_body.get("sign_up_token")
    assert response_body.get("email") == payload["email"]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "payload, expected_status_code",
    [
        pytest.param(
            {"email": "sso"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id="Not valid email",
        ),
        pytest.param(
            {"email": "another_test@mail.com"},
            status.HTTP_400_BAD_REQUEST,
            id="Email already sign up",
        ),
    ],
)
async def test_sign_up_email_error(
    payload: Dict[str, str],
    expected_status_code: int,
    another_user: UserDB,
    client: AsyncClient,
):
    response = await client.post(
        app.url_path_for("sign_up_email"), json=payload
    )
    assert response.status_code == expected_status_code


@pytest.mark.anyio
async def test_sign_up_access_code_success(
    sign_up_session_waiting_for_access_code: SignUpSessionDB,
    client: AsyncClient,
):
    token = create_access_token(
        sign_up_session_waiting_for_access_code.pk, timedelta(minutes=1)
    )
    payload = {
        "access_code": sign_up_session_waiting_for_access_code.access_code
    }
    response = await client.post(
        app.url_path_for("sign_up_access_code"),
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["email"]
        == sign_up_session_waiting_for_access_code.email
    )


@pytest.mark.anyio
@pytest.mark.parametrize(
    "payload, expected_status_code",
    [
        pytest.param(
            {"access_code": "0" * settings.app.sign_up.access_code_len},
            status.HTTP_400_BAD_REQUEST,
            id="Invalid access code",
        ),
    ],
)
async def test_sign_up_access_code_error(
    payload: Dict[str, str],
    expected_status_code: int,
    sign_up_session_waiting_for_access_code: SignUpSessionDB,
    client: AsyncClient,
):
    token = create_access_token(
        sign_up_session_waiting_for_access_code.pk, timedelta(minutes=1)
    )
    await sign_up_session_waiting_for_access_code.update(
        access_code="6" * settings.app.sign_up.access_code_len
    )
    response = await client.post(
        app.url_path_for("sign_up_access_code"),
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status_code


@pytest.mark.anyio
async def test_sign_up_name(
    sign_up_session_waiting_for_username: SignUpSessionDB, client: AsyncClient
):
    payload = {"username": "test"}
    token = create_access_token(
        sign_up_session_waiting_for_username.pk, timedelta(minutes=1)
    )
    response = await client.post(
        app.url_path_for("sign_up_name"),
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": sign_up_session_waiting_for_username.pk,
        "email": sign_up_session_waiting_for_username.email,
        "username": "test",
    }


@pytest.mark.anyio
@pytest.mark.parametrize(
    "payload, expected_status_code",
    [
        pytest.param(
            {"username": "another_test"},
            status.HTTP_400_BAD_REQUEST,
            id="Username already sign up",
        ),
    ],
)
async def test_sign_up_name_error(
    payload: Dict[str, str],
    expected_status_code: int,
    sign_up_session_waiting_for_username: SignUpSessionDB,
    another_user: UserDB,
    client: AsyncClient,
):
    token = create_access_token(
        sign_up_session_waiting_for_username.pk, timedelta(minutes=1)
    )
    response = await client.post(
        app.url_path_for("sign_up_name"),
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status_code
