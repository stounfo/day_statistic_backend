from pydantic import EmailStr

from app.common.fields import AccessCodeStr


async def send_email(*, email_to: EmailStr, access_code: AccessCodeStr):
    print(f"sent {access_code} to {email_to}")
