import re
from typing import TypedDict

from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class Password(TypedDict):
    value: str


class PasswordValidator(ABCDtoValidator[Password]):
    def validate(self, dto: Password) -> ValidationResponse:
        errors = []
        password = dto["value"]

        if not password:
            errors.append("Password is required.")
        else:
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long.")

            if not re.search(r"\d", password):
                errors.append("Password must include at least one number.")

            if not re.search(r"[A-Z]", password):
                errors.append(
                    "Password must include at least one uppercase letter.")

            if not re.search(r"[a-z]", password):
                errors.append(
                    "Password must include at least one lowercase letter.")

            if not re.search(r"[@#$%^&*()_+=!-]", password):
                errors.append(
                    "Password must include at least one special character (!@#$%^&*()-_+=)."
                )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
