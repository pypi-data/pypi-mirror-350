from ed_auth.application.features.auth.dtos.login_user_dto import LoginUserDto
from ed_auth.application.features.auth.dtos.validators.core import (
    EmailValidator, PasswordValidator, PhoneNumberValidator)
from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class LoginUserDtoValidator(ABCDtoValidator[LoginUserDto]):
    def __init__(self) -> None:
        self._email_validator = EmailValidator()
        self._password_validator = PasswordValidator()
        self._phone_number_validator = PhoneNumberValidator()

    def validate(self, dto: LoginUserDto) -> ValidationResponse:
        errors = []
        if "email" not in dto and "phone_number" not in dto:
            errors.append("Either email or phone number must be provided")

        if "phone_number" in dto:
            phone_number_validation_response = self._phone_number_validator.validate(
                {"value": dto["phone_number"]}
            )
            errors.extend(phone_number_validation_response.errors)

        if "email" in dto:
            phone_number_validation_response = self._email_validator.validate(
                {"value": dto["email"]}
            )
            errors.extend(phone_number_validation_response.errors)

        if "password" in dto:
            password_validation_response = self._password_validator.validate(
                {"value": dto["password"]}
            )
            errors.extend(password_validation_response.errors)

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
