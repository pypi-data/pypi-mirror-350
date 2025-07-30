from ed_auth.application.features.auth.dtos import CreateUserDto
from ed_auth.application.features.auth.dtos.validators.core import (
    EmailValidator, PasswordValidator, PhoneNumberValidator)
from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class CreateUserDtoValidator(ABCDtoValidator[CreateUserDto]):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, dto: CreateUserDto) -> ValidationResponse:
        errors = []
        if not dto["first_name"]:
            errors.append("First name is required")

        if not dto["last_name"]:
            errors.append("Last name is required")

        if dto.get("email") is None and dto.get("phone_number") is None:
            errors.append("Either email or phone number must be provided")

        if "email" in dto:
            email_validation_response = EmailValidator().validate(
                {"value": dto["email"]}
            )
            errors.extend(email_validation_response.errors)

        if "phone_number" in dto:
            phone_number_validation_response = PhoneNumberValidator().validate(
                {"value": dto["phone_number"]}
            )
            errors.extend(phone_number_validation_response.errors)

        if "password" in dto:
            email_validation_response = PasswordValidator().validate(
                {"value": dto["password"]}
            )
            errors.extend(email_validation_response.errors)

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
