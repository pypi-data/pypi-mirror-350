from ed_domain.documentation.message_queue.rabbitmq.abc_queue_descriptions import \
    ABCQueueDescriptions
from ed_domain.documentation.message_queue.rabbitmq.definitions.queue_description import \
    QueueDescription

from ed_auth.application.features.auth.dtos import DeleteUserDto, UpdateUserDto


class AuthQueueDescriptions(ABCQueueDescriptions):
    def __init__(self, connection_url: str) -> None:
        self._descriptions: list[QueueDescription] = [
            {
                "name": "delete_user",
                "connection_parameters": {
                    "url": connection_url,
                    "queue": "delete_user",
                },
                "durable": True,
                "request_model": DeleteUserDto,
            },
            {
                "name": "update_user",
                "connection_parameters": {
                    "url": connection_url,
                    "queue": "update_user",
                },
                "durable": True,
                "request_model": UpdateUserDto,
            },
        ]

    @property
    def descriptions(self) -> list[QueueDescription]:
        return self._descriptions
