from typing import NotRequired, TypedDict


class CreateUserDto(TypedDict):
    first_name: str
    last_name: str
    email: NotRequired[str]
    phone_number: NotRequired[str]
    password: NotRequired[str]
