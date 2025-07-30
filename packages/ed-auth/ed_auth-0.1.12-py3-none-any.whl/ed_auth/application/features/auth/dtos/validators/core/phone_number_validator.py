import re
from typing import TypedDict

from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class PhoneNumber(TypedDict):
    value: str


class PhoneNumberValidator(ABCDtoValidator[PhoneNumber]):
    def validate(self, dto: PhoneNumber) -> ValidationResponse:
        errors = []
        email = dto["value"]

        if not email:
            errors.append("Phone number is required.")
        else:
            if not re.match(r"^(\+251|0|251)?9\d{8}$", email):
                errors.append("Invalid phone number format.")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
