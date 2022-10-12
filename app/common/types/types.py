from __future__ import annotations

import re
import secrets
from typing import Dict

from pydantic.validators import str_validator

from app.common.types.errors import AccessCodeError


class AccessCodeStr(str):
    length = 6

    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: AccessCodeStr) -> AccessCodeStr:
        if any(
            [
                len(value) != cls.length,
                not re.compile(r"[0-9]").match(value),  # only digits
            ],
        ):
            raise AccessCodeError()
        return value

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, str]):
        field_schema.update(
            examples="".join((str(i) for i in range(cls.length))),
            description=(
                f"Must only contain digits and must be {cls.length} characters"
                " long"
            ),
        )

    @classmethod
    def random(cls) -> AccessCodeStr:
        return cls(
            "".join(
                [str(secrets.choice(range(10))) for i in range(cls.length)]
            )
        )


class UsernameStr(str):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: UsernameStr) -> UsernameStr:
        if not any(map(str.isalpha, value)) or not re.compile(
            r"^[A-z 0-9]{4,16}$"
        ).match(value):
            raise AccessCodeError()
        return value

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, str]):
        field_schema.update(
            examples="1234u",
            description=(
                "UsernameStr has contain at least one letter"
                "and has to have length between 4 and 16"
            ),
        )
