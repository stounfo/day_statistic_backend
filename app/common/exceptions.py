from typing import Any

from fastapi import HTTPException, status


class APIException(HTTPException):
    """
    Light wrapper around HTTPException that allows
    specifying defaults via class property
    """

    status_code = status.HTTP_400_BAD_REQUEST

    detail = None
    headers = None

    def __init__(self, *args: Any, **kwargs: Any):
        if "status_code" not in kwargs:
            kwargs["status_code"] = self.status_code
        if "detail" not in kwargs:
            kwargs["detail"] = self.detail
        if "headers" not in kwargs:
            kwargs["headers"] = self.headers
        super().__init__(*args, **kwargs)


class EmailAlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The user with this email already exists in the system."


class InvalidAccessCodeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid access code."


class EmailNotValidatedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The user doesn't validate the email"


class UsernameAlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The user with this username already exists in the system."
