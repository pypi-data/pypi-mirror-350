from typing import Any, Type, Unpack

from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from pydantic import BaseModel

from quick_jwt.core._function_args import ModelValidateKwargs
from quick_jwt.core.abc import IDecodeDriverJWT, BaseJWT, IEncodeDriverJWT
from quick_jwt.dto import JWTTokensDTO


class PyJWTDecodeDriverJWT(IDecodeDriverJWT, BaseJWT):
    def _get_payload(
        self,
        bearer_token: HTTPAuthorizationCredentials | None,
        cookie_token: str | None,
    ) -> Any:
        self._validate_driver()
        config = self._get_config()

        token = None
        if bearer_token is not None and bearer_token.credentials is not None:
            token = bearer_token.credentials
        if cookie_token is not None:
            token = cookie_token
        if token is None:
            raise config.build_unauthorized_http_exception()

        try:
            payload = config.driver.decode(token, **config.build_decode_params())
        except InvalidTokenError:
            raise config.build_unauthorized_http_exception()

        return payload

    def _get_payload_optional(
        self,
        bearer_token: HTTPAuthorizationCredentials | None,
        cookie_token: str | None,
    ) -> Any | None:
        self._validate_driver()
        config = self._get_config()

        token = None
        if bearer_token is not None and bearer_token.credentials is not None:
            token = bearer_token.credentials
        if cookie_token is not None:
            token = cookie_token
        if token is None:
            return None

        try:
            payload = config.driver.decode(token, **config.build_decode_params())
        except InvalidTokenError:
            return None

        return payload

    def _validate_driver(self) -> None:
        config = self._get_config()

        if hasattr(config.driver, 'decode') is False or hasattr(config.driver, 'encode') is False:
            raise Exception(
                """
                QuickJWTConfig.driver received invalid driver. 
                Driver should have decode function.
                Default driver: PyJWT()
                """
            )


class PyJWTEncodeDriverJWT(IEncodeDriverJWT, BaseJWT):
    def __init__(
        self,
        access_payload: Type[BaseModel],
        refresh_payload: Type[BaseModel],
        **model_validate_kwargs: Unpack[ModelValidateKwargs],
    ):
        self._access_payload = access_payload
        self._refresh_payload = refresh_payload
        self._model_validate_kwargs = model_validate_kwargs

        super().__init__()

    async def create_jwt_tokens(
        self,
        access_payload: BaseModel,
        refresh_payload: BaseModel,
    ) -> JWTTokensDTO:
        access_token = await self.create_access_token(access_payload)
        refresh_token = await self.create_refresh_token(refresh_payload)

        return JWTTokensDTO(
            access=access_token,
            refresh=refresh_token,
        )

    async def create_access_token(self, access_payload: BaseModel) -> str:
        self._validate_driver()
        config = self._get_config()
        response = self._get_response()

        access_payload = self._access_payload.model_validate(access_payload, **self._model_validate_kwargs)
        access_token = config.driver.encode(access_payload.model_dump(mode='json'), **config.build_encode_params())
        response.set_cookie(value=access_token, **config.build_access_token_params())
        return access_token

    async def create_refresh_token(self, refresh_payload: BaseModel) -> str:
        self._validate_driver()
        config = self._get_config()
        response = self._get_response()

        refresh_payload = self._refresh_payload.model_validate(refresh_payload, **self._model_validate_kwargs)
        refresh_token = config.driver.encode(refresh_payload.model_dump(mode='json'), **config.build_encode_params())
        response.set_cookie(value=refresh_token, **config.build_refresh_token_params())
        return refresh_token

    def _validate_driver(self) -> None:
        config = self._get_config()

        if hasattr(config.driver, 'decode') is False or hasattr(config.driver, 'encode') is False:
            raise Exception(
                """
                QuickJWTConfig.driver received invalid driver. 
                Driver should have decode function.
                Default driver: PyJWT()
                """
            )
