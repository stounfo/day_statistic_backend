from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.common.models import TokenPayload
from app.user.models.sign_up import SignUpSessionDB


async def get_current_sign_up_session(
    sign_up_token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> SignUpSessionDB:
    token = TokenPayload(**eval(sign_up_token.credentials))
    return await SignUpSessionDB.get(token.sub)
