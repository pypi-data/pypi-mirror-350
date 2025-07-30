from typing import NotRequired, TypedDict


class UpdateUserDto(TypedDict):
    id: str
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    phone_number: NotRequired[str]
    password: NotRequired[str]
    email: NotRequired[str]
