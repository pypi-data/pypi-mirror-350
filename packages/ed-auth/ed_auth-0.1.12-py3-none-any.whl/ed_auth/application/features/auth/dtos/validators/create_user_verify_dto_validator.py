from ed_auth.application.features.auth.dtos.create_user_verify_dto import \
    CreateUserVerifyDto
from ed_auth.application.features.auth.dtos.validators.core import OtpValidator
from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class CreateUserVerifyDtoValidator(ABCDtoValidator[CreateUserVerifyDto]):
    def __init__(self) -> None:
        self._otp_validator = OtpValidator()

    def validate(self, dto: CreateUserVerifyDto) -> ValidationResponse:
        errors = []
        if not dto["user_id"]:
            errors.append("User ID is required")

        otp_validation_response = self._otp_validator.validate(
            {"value": dto["otp"]})
        errors.extend(otp_validation_response.errors)

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
