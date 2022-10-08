from typing import Type

import pytest
from pydantic import BaseModel, ValidationError

from app.common.types import AccessCodeStr
from app.config import settings


def test_sign_up_access_code_str():
    class Model(BaseModel):
        v: AccessCodeStr

    assert (
        Model(
            v=AccessCodeStr("0" * settings.app.user_settings.access_code_len)
        ).v
        == "0" * settings.app.user_settings.access_code_len
    )


@pytest.mark.parametrize(
    "value, expected_exception",
    [
        pytest.param(
            "0" * (settings.app.user_settings.access_code_len + 1),
            ValidationError,
            id="Is longer",
        ),
        pytest.param(
            "0" * (settings.app.user_settings.access_code_len - 1),
            ValidationError,
            id="Is shorter",
        ),
        pytest.param(
            "s" * settings.app.user_settings.access_code_len,
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
