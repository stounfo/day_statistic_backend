from pydantic import PydanticValueError


class AccessCodeError(PydanticValueError):
    msg_template = "value is not a valid access code"
