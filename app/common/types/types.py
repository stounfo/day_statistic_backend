from __future__ import annotations

import re
from typing import Dict, TypeAlias

from pydantic.validators import str_validator

from app.common.types.errors import AccessCodeError
from app.config import settings


class AccessCodeStr(str):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: AccessCodeStr) -> AccessCodeStr:
        if any(
            [
                len(value) != settings.app.user_settings.access_code_len,
                not re.compile(r"[0-9]").match(value),  # only digits
            ],
        ):
            raise AccessCodeError()
        return value

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, str]):
        field_schema.update(
            examples="".join(
                (
                    str(i)
                    for i in range(settings.app.user_settings.access_code_len)
                )
            ),
            description=(
                "Must only contain digits and must be"
                f" {settings.app.user_settings.access_code_len} characters"
                " long"
            ),
        )

class UsernameStr(str):     
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield cls.validate
    
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, str]):
        field_schema.update(
            examples="1234u",
            description=(
                "UsernameStr has contain at least one letter \
                    and has to have length between 4 and 16"
            ),
        )

    
    @classmethod
    def validate(cls, value: UsernameStr) -> UsernameStr:
        if any(map(str.isalpha, value)) == False or value != re.compile(r"^[A-z 0-9]{4,16}$"):
            raise AccessCodeError()
        return value