import re
from typing import TypedDict

from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class Email(TypedDict):
    value: str


class EmailValidator(ABCDtoValidator[Email]):
    def validate(self, dto: Email) -> ValidationResponse:
        errors = []
        email = dto["value"]

        if not email:
            errors.append("Email is required.")
        else:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("Invalid email format.")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
