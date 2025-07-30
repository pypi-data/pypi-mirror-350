from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.entities.otp import OtpVerificationAction
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.tokens.auth_payload import AuthPayload, UserType
from ed_domain.utils.jwt import ABCJwtHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos import UserDto
from ed_auth.application.features.auth.dtos.validators import \
    LoginUserVerifyDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    LoginUserVerifyCommand

LOG = get_logger()


@request_handler(LoginUserVerifyCommand, BaseResponse[UserDto])
class LoginUserVerifyCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, jwt: ABCJwtHandler):
        self._uow = uow
        self._jwt = jwt
        self._dto_validator = LoginUserVerifyDtoValidator()

    async def handle(self, request: LoginUserVerifyCommand) -> BaseResponse[UserDto]:
        dto_validator = self._dto_validator.validate(request.dto)

        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Login failed.",
                dto_validator.errors,
            )

        dto = request.dto
        user = self._uow.auth_user_repository.get(id=dto["user_id"])
        if not user:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Login failed.",
                [f"User with that id = {dto['user_id']} does not exist."],
            )

        otp = self._uow.otp_repository.get(user_id=dto["user_id"])
        if not otp or otp["action"] != OtpVerificationAction.LOGIN:
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Login failed.",
                [
                    f"Otp has not been sent to the user with id = {dto['user_id']} recently."
                ],
            )

        if otp["value"] != dto["otp"]:
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Login failed.",
                ["Otp does not match with the one sent."],
            )

        token = self._jwt.encode(
            AuthPayload(
                first_name=user["first_name"],
                last_name=user["last_name"],
                email=user.get("email", ""),
                phone_number=user.get("phone_number", ""),
                user_type=UserType.DRIVER,
            )
        )

        user["logged_in"] = True
        self._uow.auth_user_repository.update(user["id"], user)

        return BaseResponse[UserDto].success(
            "Login successful.",
            UserDto(
                **user,  # type: ignore
                token=token,
            ),
        )
