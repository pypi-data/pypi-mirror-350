from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.entities import AuthUser
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.utils.security.password import ABCPasswordHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos import UnverifiedUserDto
from ed_auth.application.features.auth.dtos.update_user_dto import \
    UpdateUserDto
from ed_auth.application.features.auth.dtos.user_dto import UserDto
from ed_auth.application.features.auth.dtos.validators import \
    UpdateUserDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    UpdateUserCommand

LOG = get_logger()


@request_handler(UpdateUserCommand, BaseResponse[UserDto])
class UpdateUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, password: ABCPasswordHandler):
        self._uow = uow
        self._dto_validator = UpdateUserDtoValidator()
        self._password = password

    async def handle(self, request: UpdateUserCommand) -> BaseResponse[UserDto]:
        validation_response = self._dto_validator.validate(request.dto)

        if not validation_response.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Creating account failed.",
                validation_response.errors,
            )

        if user := self._uow.auth_user_repository.get(id=request.id):
            dto = request.dto
            self._uow.auth_user_repository.update(
                id=user["id"],
                entity=AuthUser(
                    id=user["id"],
                    create_datetime=user["create_datetime"],
                    update_datetime=datetime.now(UTC),
                    deleted=user["deleted"],
                    first_name=self._get_from_dto_or_user(
                        user, dto, "first_name"),
                    last_name=self._get_from_dto_or_user(
                        user, dto, "last_name"),
                    email=self._get_from_dto_or_user(user, dto, "email"),
                    phone_number=self._get_from_dto_or_user(
                        user, dto, "phone_number"),
                    password_hash=self._get_from_dto_or_user(
                        user, dto, "password_hash"
                    ),
                    verified=user["verified"],
                    logged_in=user["logged_in"],
                ),
            )

            return BaseResponse[UserDto].success(
                "User updated successfully.",
                UserDto(**user),  # type: ignore
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "User update failed.",
            ["User not found."],
        )

    def _get_from_dto_or_user(
        self,
        user: AuthUser,
        dto: UpdateUserDto,
        key: str,
    ) -> str:
        if key != "password":
            return dto[key] if key in dto else user[key] if key in user else ""

        return (
            self._password.hash(dto[key])
            if key in dto
            else user[key] if key in user else ""
        )
