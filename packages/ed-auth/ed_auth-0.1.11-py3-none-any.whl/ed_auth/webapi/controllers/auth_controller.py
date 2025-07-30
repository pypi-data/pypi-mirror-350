from ed_domain.common.logging import get_logger
from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from ed_auth.application.features.auth.dtos import (CreateUserDto,
                                                    CreateUserVerifyDto,
                                                    LoginUserDto,
                                                    LoginUserVerifyDto,
                                                    LogoutDto,
                                                    UnverifiedUserDto, UserDto,
                                                    VerifyTokenDto)
from ed_auth.application.features.auth.requests.commands import (
    CreateUserCommand, CreateUserVerifyCommand, LoginUserCommand,
    LoginUserVerifyCommand, LogoutUserCommand, VerifyTokenCommand)
from ed_auth.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_auth.webapi.dependency_setup import mediator

ROUTER = APIRouter(prefix="/auth", tags=["Auth"])
LOG = get_logger()


@ROUTER.post("/create/get-otp", response_model=GenericResponse[UnverifiedUserDto])
@rest_endpoint
async def create_user_get_otp(
    request: CreateUserDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(CreateUserCommand(dto=request))


@ROUTER.post("/create/verify-otp", response_model=GenericResponse[UserDto])
@rest_endpoint
async def create_user_verify_otp(
    request: CreateUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(CreateUserVerifyCommand(dto=request))


@ROUTER.post("/login/get-otp", response_model=GenericResponse[UnverifiedUserDto])
@rest_endpoint
async def login_get_otp(
    request: LoginUserDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginUserCommand(dto=request))


@ROUTER.post("/login/verify-otp", response_model=GenericResponse[UserDto])
@rest_endpoint
async def login_verify_otp(
    request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginUserVerifyCommand(dto=request))


@ROUTER.post("/token/verify", response_model=GenericResponse[UserDto])
@rest_endpoint
async def token(
    request: VerifyTokenDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(VerifyTokenCommand(dto=request))


@ROUTER.post("/logout", response_model=GenericResponse[UserDto])
@rest_endpoint
async def logout(
    request: LogoutDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(LogoutUserCommand(dto=request))
