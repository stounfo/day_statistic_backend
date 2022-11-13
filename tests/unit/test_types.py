from typing import Type

import pytest
from pydantic import BaseModel, ValidationError

from app.common.types import AccessCodeStr, UsernameStr


def test_sign_up_access_code_str():
    class Model(BaseModel):
        v: AccessCodeStr

    assert (
        Model(v=AccessCodeStr("0" * AccessCodeStr.length)).v
        == "0" * AccessCodeStr.length
    )


def test_sign_up_access_code_str_random():
    access_code = AccessCodeStr.random()
    assert len(access_code) == AccessCodeStr.length


@pytest.mark.parametrize(
    "value, expected_exception",
    [
        pytest.param(
            "0" * (AccessCodeStr.length + 1),
            ValidationError,
            id="Is longer",
        ),
        pytest.param(
            "0" * (AccessCodeStr.length - 1),
            ValidationError,
            id="Is shorter",
        ),
        pytest.param(
            "s" * AccessCodeStr.length,
            ValidationError,
            id="Not valid characters",
        ),
    ],
)
def test_sign_up_access_code_str_errors(
    value: str, expected_exception: Type[Exception]
):
    class Model(BaseModel):
        v: AccessCodeStr

    with pytest.raises(expected_exception):
        Model(v=AccessCodeStr(value))


@pytest.mark.parametrize(
    "value, expected_value",
    [
        pytest.param("username", "username"),
        pytest.param("username1", "username1"),
    ],
)
def test_username_str_success(value: str, expected_value: str):
    class Model(BaseModel):
        v: UsernameStr

    assert Model(v=UsernameStr(value)).v == expected_value


@pytest.mark.parametrize(
    "value, expected_exception",
    [
        pytest.param(
            "usernameusernameu",
            ValidationError,
            id="Is longer",
        ),
        pytest.param(
            "use",
            ValidationError,
            id="Is shorter",
        ),
        pytest.param(
            "123456",
            ValidationError,
            id="Only digits",
        ),
        pytest.param(
            "тестюзер",
            ValidationError,
            id="Not valid characters",
        ),
        pytest.param(
            "user/",
            ValidationError,
            id="Invalid symbol",
        ),
    ],
)
def test_username_str_errors(value: str, expected_exception: Type[Exception]):
    class Model(BaseModel):
        v: UsernameStr

    with pytest.raises(expected_exception):
        Model(v=UsernameStr(value))
