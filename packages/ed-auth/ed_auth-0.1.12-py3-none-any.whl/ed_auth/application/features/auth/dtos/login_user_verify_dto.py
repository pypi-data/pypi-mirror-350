from typing import TypedDict
from uuid import UUID


class LoginUserVerifyDto(TypedDict):
    user_id: UUID
    otp: str
