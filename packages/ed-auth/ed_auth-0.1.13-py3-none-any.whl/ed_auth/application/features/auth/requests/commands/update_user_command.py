from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos import UpdateUserDto, UserDto


@request(BaseResponse[UserDto])
@dataclass
class UpdateUserCommand(Request):
    id: UUID
    dto: UpdateUserDto
