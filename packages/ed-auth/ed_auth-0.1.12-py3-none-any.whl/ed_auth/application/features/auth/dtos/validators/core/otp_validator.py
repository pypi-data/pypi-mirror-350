from typing import TypedDict

from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class Otp(TypedDict):
    value: str


class OtpValidator(ABCDtoValidator[Otp]):
    def validate(self, dto: Otp) -> ValidationResponse:
        errors = []

        otp = dto["value"]
        if not otp.isnumeric():
            errors.append("OTP must be numeric.")

        if len(otp) != 4:
            errors.append("OTP must be 4 numbers.")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
