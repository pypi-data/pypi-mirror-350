from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.entities import AuthUser, Otp
from ed_domain.core.entities.notification import NotificationType
from ed_domain.core.entities.otp import OtpVerificationAction
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.utils.otp import ABCOtpGenerator
from ed_domain.utils.security.password import ABCPasswordHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.contracts.infrastructure.abc_api import ABCApi
from ed_auth.application.features.auth.dtos import UnverifiedUserDto
from ed_auth.application.features.auth.dtos.validators import \
    CreateUserDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    CreateUserCommand
from ed_auth.common.generic_helpers import get_new_id

LOG = get_logger()


@request_handler(CreateUserCommand, BaseResponse[UnverifiedUserDto])
class CreateUserCommandHandler(RequestHandler):
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
        self._dto_validator = CreateUserDtoValidator()

    async def handle(
        self, request: CreateUserCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        validation_response = self._dto_validator.validate(request.dto)

        print(self._dto_validator)
        if not validation_response.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Creating account failed.",
                validation_response.errors,
            )

        dto = request.dto
        hashed_password = (
            self._password.hash(dto["password"]) if "password" in dto else ""
        )
        user = self._uow.auth_user_repository.create(
            AuthUser(
                id=get_new_id(),
                first_name=dto["first_name"],
                last_name=dto["last_name"],
                email=dto.get("email", ""),
                phone_number=dto.get("phone_number", ""),
                password_hash=hashed_password,
                verified=False,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted=False,
                logged_in=False,
            )
        )

        created_otp = self._uow.otp_repository.create(
            Otp(
                id=get_new_id(),
                user_id=user["id"],
                action=OtpVerificationAction.VERIFY_EMAIL,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                expiry_datetime=datetime.now(UTC),
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
                "Creating account failed.",
                ["Failed to send OTP."],
            )

        return BaseResponse[UnverifiedUserDto].success(
            "User created successfully. Verify email.",
            UnverifiedUserDto(**user),  # type: ignore
        )
