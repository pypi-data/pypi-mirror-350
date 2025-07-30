from typing import Annotated
from uuid import UUID

from ed_domain.common.logging import get_logger
from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit.schemas import RabbitQueue
from rmediator.mediator import Mediator

from ed_auth.application.features.auth.dtos import DeleteUserDto, UpdateUserDto
from ed_auth.application.features.auth.requests.commands import (
    DeleteUserCommand, UpdateUserCommand)
from ed_auth.common.generic_helpers import get_config
from ed_auth.webapi.dependency_setup import mediator

config = get_config()
router = RabbitRouter(config["rabbitmq"]["url"])
delete_user_queue = RabbitQueue(name="delete_user", durable=True)
update_user_queue = RabbitQueue(name="update_user", durable=True)

LOG = get_logger()


@router.subscriber(delete_user_queue)
async def delete_user(
    delete_user_dto: DeleteUserDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(DeleteUserCommand(delete_user_dto["id"]))


@router.subscriber(update_user_queue)
async def update_user(
    update_user_dto: UpdateUserDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(
        UpdateUserCommand(UUID(update_user_dto["id"]), update_user_dto)
    )
