from typing import NotRequired, TypedDict


class LoginUserDto(TypedDict):
    email: NotRequired[str]
    phone_number: NotRequired[str]
    password: NotRequired[str]
