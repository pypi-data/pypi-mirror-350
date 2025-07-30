from typing import Annotated, Type, Unpack

from fastapi import Depends
from pydantic import BaseModel

from quick_jwt.core._function_args import ModelValidateKwargs
from quick_jwt.authentication import (
    CreateJWT,
    RefreshJWT,
    RefreshTokenCheck,
    LogoutJWT,
    AccessTokenOptionalCheck,
    RefreshTokenOptionalCheck,
    AccessTokenCheck,
)


def create_jwt_depends[
    AccessPayloadType: Type[BaseModel],
    RefreshPayloadType: Type[BaseModel],
](
    access_payload: AccessPayloadType,
    refresh_payload: RefreshPayloadType,
    **_model_validate_kwargs: Unpack[ModelValidateKwargs],
) -> Type[CreateJWT]:
    depends = CreateJWT(access_payload, refresh_payload, **_model_validate_kwargs)
    return Annotated[CreateJWT, Depends(depends)]  # type: ignore


def access_check_depends[PayloadModelType: Type[BaseModel]](
    payload_model: PayloadModelType,
    **_model_validate_kwargs: Unpack[ModelValidateKwargs],
) -> PayloadModelType:
    depends = AccessTokenCheck(payload_model, **_model_validate_kwargs)
    return Annotated[PayloadModelType, Depends(depends)]  # type: ignore


def refresh_check_depends[PayloadModelType: Type[BaseModel]](
    payload_model: PayloadModelType,
    **_model_validate_kwargs: Unpack[ModelValidateKwargs],
) -> PayloadModelType:
    depends = RefreshTokenCheck(payload_model, **_model_validate_kwargs)
    return Annotated[PayloadModelType, Depends(depends)]  # type: ignore


def refresh_jwt_depends[
    AccessTokenPayloadType: Type[BaseModel],
    RefreshTokenPayloadType: Type[BaseModel],
](
    access_token_payload: AccessTokenPayloadType,
    refresh_token_payload: RefreshTokenPayloadType,
    **response_model_validate_kwargs: Unpack[ModelValidateKwargs],
) -> Type[RefreshJWT]:
    depends = RefreshJWT(access_token_payload, refresh_token_payload, **response_model_validate_kwargs)
    return Annotated[Type[RefreshJWT], Depends(depends)]  # type: ignore


def logout_depends() -> None:
    depends = LogoutJWT()
    return Annotated[None, Depends(depends)]  # type: ignore


def access_check_optional_depends[PayloadModelType: Type[BaseModel]](
    payload_model: PayloadModelType,
    **_model_validate_kwargs: Unpack[ModelValidateKwargs],
) -> PayloadModelType | None:
    depends = AccessTokenOptionalCheck(payload_model, **_model_validate_kwargs)
    return Annotated[PayloadModelType | None, Depends(depends)]  # type: ignore


def refresh_check_optional_depends[PayloadModelType: Type[BaseModel]](
    payload_model: PayloadModelType,
    **_model_validate_kwargs: Unpack[ModelValidateKwargs],
) -> PayloadModelType | None:
    depends = RefreshTokenOptionalCheck(payload_model, **_model_validate_kwargs)
    return Annotated[PayloadModelType | None, Depends(depends)]  # type: ignore
