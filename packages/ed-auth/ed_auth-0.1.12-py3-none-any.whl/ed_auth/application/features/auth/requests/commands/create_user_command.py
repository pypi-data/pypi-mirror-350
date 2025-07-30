from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos import CreateUserDto, UnverifiedUserDto


@request(BaseResponse[UnverifiedUserDto])
@dataclass
class CreateUserCommand(Request):
    dto: CreateUserDto
