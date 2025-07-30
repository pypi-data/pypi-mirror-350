from abc import ABCMeta, abstractmethod

from ed_auth.application.features.auth.dtos import DeleteUserDto, UpdateUserDto


class ABCAuthRabbitMQSubscriber(metaclass=ABCMeta):
    @abstractmethod
    def delete_user(self, delete_user_dto: DeleteUserDto) -> None: ...

    @abstractmethod
    def update_user(self, update_user_dto: UpdateUserDto) -> None: ...
