from typing import TypedDict
from uuid import UUID


class CreateUserVerifyDto(TypedDict):
    user_id: UUID
    otp: str
