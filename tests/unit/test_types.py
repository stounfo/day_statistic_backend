from typing import Type

import pytest
from pydantic import BaseModel, ValidationError

from app.common.types import AccessCodeStr


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
