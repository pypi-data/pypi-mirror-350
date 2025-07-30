from datetime import UTC, datetime, timedelta

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.entities import Otp
from ed_domain.core.entities.notification import NotificationType
from ed_domain.core.entities.otp import OtpVerificationAction
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.utils.otp import ABCOtpGenerator
from ed_domain.utils.security.password import ABCPasswordHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.contracts.infrastructure.abc_api import ABCApi
from ed_auth.application.features.auth.dtos.unverified_user_dto import \
    UnverifiedUserDto
from ed_auth.application.features.auth.dtos.validators.login_user_dto_validator import \
    LoginUserDtoValidator
from ed_auth.application.features.auth.requests.commands.login_user_command import \
    LoginUserCommand
from ed_auth.common.generic_helpers import get_new_id

LOG = get_logger()


@request_handler(LoginUserCommand, BaseResponse[UnverifiedUserDto])
class LoginUserCommandHandler(RequestHandler):
    def __init__(
        self,
        api: ABCApi,
        uow: ABCUnitOfWork,
        otp: ABCOtpGenerator,
        password: ABCPasswordHandler,
    ):
        self._api = api
        self._uow = uow
        self._otp = otp
        self._password = password
        self._dto_validator = LoginUserDtoValidator()

    async def handle(
        self, request: LoginUserCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        dto_validator = self._dto_validator.validate(request.dto)

        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Login failed.",
                dto_validator.errors,
            )

        email, phone_number = request.dto.get("email", ""), request.dto.get(
            "phone_number", ""
        )
        user = (
            self._uow.auth_user_repository.get(email=email)
            if email
            else self._uow.auth_user_repository.get(phone_number=phone_number)
        )

        if not user:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Login failed.",
                ["No user found with the given credentials."],
            )

        if user["password_hash"]:
            if "password" not in request.dto:
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    "Login failed.",
                    ["Password is required."],
                )

            if not self._password.verify(
                request.dto["password"], user["password_hash"]
            ):
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    "Login failed.",
                    ["Password is incorrect."],
                )

        if previously_sent_otp := self._uow.otp_repository.get(user_id=user["id"]):
            self._uow.otp_repository.delete(previously_sent_otp["id"])

        created_otp = self._uow.otp_repository.create(
            Otp(
                id=get_new_id(),
                user_id=user["id"],
                action=OtpVerificationAction.LOGIN,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                expiry_datetime=datetime.now(UTC) + timedelta(minutes=2),
                value=self._otp.generate(),
                deleted=False,
            )
        )

        notification_response = self._api.notification_api.send_notification(
            {
                "user_id": user["id"],
                "message": f"Your OTP for logging in is {created_otp['value']}",
                "notification_type": NotificationType.EMAIL,
            }
        )
        if not notification_response["is_success"]:
            LOG.error(
                f"Failed to send OTP to user {user['id']}: {notification_response['errors']}"
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Login failed.",
                ["Failed to send OTP."],
            )

        return BaseResponse[UnverifiedUserDto].success(
            "Otp sent successfully.",
            UnverifiedUserDto(**user),  # type: ignore
        )
