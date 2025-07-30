from abc import ABCMeta, abstractmethod

from ed_notification.documentation.api.abc_notification_api_client import \
    ABCNotificationApiClient


class ABCApi(metaclass=ABCMeta):
    @property
    @abstractmethod
    def notification_api(self) -> ABCNotificationApiClient: ...
