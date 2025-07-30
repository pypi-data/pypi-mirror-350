from typing import Type, Unpack, Self

from fastapi import Request, Response
from pydantic import BaseModel

from quick_jwt.core._function_args import ModelValidateKwargs
from quick_jwt.core.abc import BaseJWT
from quick_jwt.core.drivers import PyJWTDecodeDriverJWT, PyJWTEncodeDriverJWT
from quick_jwt.core.security import access_bearer_security, refresh_bearer_security


class CreateJWT(PyJWTEncodeDriverJWT):
    async def __call__(
        self,
        request: Request,
        response: Response,
    ) -> Self:
        self._setup_call_function_params(request, response)
        return self


class AccessTokenCheck(PyJWTDecodeDriverJWT):
    __slots__ = (
        '_payload_model',
        '_model_validate_kwargs',
    )

    def __init__(
        self,
        payload_model: Type[BaseModel],
        **model_validate_kwargs: Unpack[ModelValidateKwargs],
    ):
        self._payload_model = payload_model
        self._model_validate_kwargs = model_validate_kwargs

        super().__init__()

    async def __call__(
        self,
        request: Request,
        response: Response,
        bearer_token: access_bearer_security,
    ) -> BaseModel:
        self._setup_call_function_params(request, response)
        config = self._get_config()

        cookie_token = request.cookies.get(config.access_token_name)
        raw_payload = self._get_payload(bearer_token, cookie_token)

        return self._payload_model.model_validate(raw_payload, **self._model_validate_kwargs)


class RefreshTokenCheck(PyJWTDecodeDriverJWT):
    __slots__ = (
        '_payload_model',
        '_model_validate_kwargs',
    )

    def __init__(
        self,
        payload_model: Type[BaseModel],
        **model_validate_kwargs: Unpack[ModelValidateKwargs],
    ) -> None:
        self._payload_model = payload_model
        self._model_validate_kwargs = model_validate_kwargs

        super().__init__()

    async def __call__(
        self,
        request: Request,
        response: Response,
        bearer_token: refresh_bearer_security,
    ) -> BaseModel:
        self._setup_call_function_params(request, response)
        config = self._get_config()

        cookie_token = request.cookies.get(config.refresh_token_name)
        raw_payload = self._get_payload(bearer_token, cookie_token)

        return self._payload_model.model_validate(raw_payload, **self._model_validate_kwargs)


class RefreshJWT(PyJWTEncodeDriverJWT, PyJWTDecodeDriverJWT):
    __slots__ = ('payload',)

    def __init__(
        self,
        access_payload: Type[BaseModel],
        refresh_payload: Type[BaseModel],
        **model_validate_kwargs: Unpack[ModelValidateKwargs],
    ) -> None:
        super().__init__(access_payload, refresh_payload, **model_validate_kwargs)

        self.payload: BaseModel | None = None

    async def __call__(
        self,
        request: Request,
        response: Response,
        bearer_token: refresh_bearer_security,
    ) -> Self:
        self._setup_call_function_params(request, response)
        config = self._get_config()

        cookie_token = request.cookies.get(config.refresh_token_name)
        self.payload = self._get_payload(bearer_token, cookie_token)

        return self


class LogoutJWT(BaseJWT):
    async def __call__(
        self,
        request: Request,
        response: Response,
        bearer_token: access_bearer_security,
    ) -> None:
        self._setup_call_function_params(request, response)
        config = self._get_config()

        response.delete_cookie(config.access_token_name)
        response.delete_cookie(config.refresh_token_name)


class AccessTokenOptionalCheck(PyJWTDecodeDriverJWT):
    __slots__ = (
        '_payload_model',
        '_model_validate_kwargs',
    )

    def __init__(
        self,
        payload_model: Type[BaseModel],
        **model_validate_kwargs: Unpack[ModelValidateKwargs],
    ) -> None:
        self._payload_model = payload_model
        self._model_validate_kwargs = model_validate_kwargs

        super().__init__()

    async def __call__(
        self,
        request: Request,
        response: Response,
        bearer_token: access_bearer_security,
    ) -> BaseModel | None:
        self._setup_call_function_params(request, response)
        config = self._get_config()

        cookie_token = request.cookies.get(config.access_token_name)
        raw_payload = self._get_payload_optional(bearer_token, cookie_token)
        if raw_payload is None:
            return None

        return self._payload_model.model_validate(raw_payload, **self._model_validate_kwargs)


class RefreshTokenOptionalCheck(PyJWTDecodeDriverJWT):
    __slots__ = (
        '_payload_model',
        '_model_validate_kwargs',
    )

    def __init__(
        self,
        payload_model: Type[BaseModel],
        **model_validate_kwargs: Unpack[ModelValidateKwargs],
    ) -> None:
        self._payload_model = payload_model
        self._model_validate_kwargs = model_validate_kwargs

        super().__init__()

    async def __call__(
        self,
        request: Request,
        response: Response,
        bearer_token: refresh_bearer_security,
    ) -> BaseModel | None:
        self._setup_call_function_params(request, response)
        config = self._get_config()

        cookie_token = request.cookies.get(config.refresh_token_name)
        raw_payload = self._get_payload_optional(bearer_token, cookie_token)
        if raw_payload is None:
            return None

        return self._payload_model.model_validate(raw_payload, **self._model_validate_kwargs)
