from uuid import UUID

from ed_domain.common.logging import get_logger
from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from ed_auth.application.features.auth.dtos import UpdateUserDto
from ed_auth.application.features.auth.requests.commands import (
    DeleteUserCommand, UpdateUserCommand)
from ed_auth.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_auth.webapi.dependency_setup import mediator

router = APIRouter(prefix="/users", tags=["Users"])
LOG = get_logger()


@router.delete("/{id}", response_model=GenericResponse[None])
@rest_endpoint
async def delete_user(id: UUID, mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(DeleteUserCommand(id))


@router.patch("/{id}", response_model=GenericResponse[None])
@rest_endpoint
async def update_user(
    id: UUID, dto: UpdateUserDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(UpdateUserCommand(id, dto))
