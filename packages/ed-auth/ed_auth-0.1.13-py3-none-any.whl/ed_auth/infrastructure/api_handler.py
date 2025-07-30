from ed_notification.documentation.api.abc_notification_api_client import \
    ABCNotificationApiClient

from ed_auth.application.contracts.infrastructure.abc_api import ABCApi


class ApiHandler(ABCApi):
    def __init__(self, notification_api: ABCNotificationApiClient) -> None:
        self._notification_api = notification_api

    @property
    def notification_api(self) -> ABCNotificationApiClient:
        return self._notification_api
