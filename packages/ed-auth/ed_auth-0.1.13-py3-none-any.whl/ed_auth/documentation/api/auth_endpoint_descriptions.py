from ed_domain.documentation.api.abc_endpoint_descriptions import \
    ABCEndpointDescriptions
from ed_domain.documentation.api.definitions import (EndpointDescription,
                                                     HttpMethod)

from ed_auth.application.features.auth.dtos import (CreateUserDto,
                                                    CreateUserVerifyDto,
                                                    LoginUserDto,
                                                    LoginUserVerifyDto,
                                                    LogoutDto,
                                                    UnverifiedUserDto, UserDto,
                                                    VerifyTokenDto)
from ed_auth.application.features.auth.dtos.update_user_dto import \
    UpdateUserDto


class AuthEndpointDescriptions(ABCEndpointDescriptions):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._descriptions: list[EndpointDescription] = [
            # Auth endpoints
            {
                "name": "create_get_otp",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/auth/create/get-otp",
                "request_model": CreateUserDto,
                "response_model": UnverifiedUserDto,
            },
            {
                "name": "create_verify_otp",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/auth/create/verify-otp",
                "request_model": CreateUserVerifyDto,
                "response_model": UserDto,
            },
            {
                "name": "login_get_otp",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/auth/login/get-otp",
                "request_model": LoginUserDto,
                "response_model": UnverifiedUserDto,
            },
            {
                "name": "login_verify_otp",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/auth/login/verify-otp",
                "request_model": LoginUserVerifyDto,
                "response_model": UserDto,
            },
            {
                "name": "verify_token",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/auth/token/verify",
                "request_model": VerifyTokenDto,
                "response_model": UserDto,
            },
            {
                "name": "logout",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/logout",
                "request_model": LogoutDto,
            },
            # User endpoints
            {
                "name": "delete_user",
                "method": HttpMethod.DELETE,
                "path": f"{self._base_url}/users/{{user_id}}",
                "path_params": {"user_id": str},
            },
            {
                "name": "update_user",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/users/{{user_id}}",
                "path_params": {"user_id": str},
                "request_model": UpdateUserDto,
                "response_model": UserDto,
            },
        ]

    @property
    def descriptions(self) -> list[EndpointDescription]:
        return self._descriptions
