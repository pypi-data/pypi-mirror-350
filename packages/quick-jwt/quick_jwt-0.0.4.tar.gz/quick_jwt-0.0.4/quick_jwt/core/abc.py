import abc
from typing import Any

from fastapi import Request, Response
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from quick_jwt import QuickJWTConfig
from quick_jwt.dto import JWTTokensDTO


class IDecodeDriverJWT(metaclass=abc.ABCMeta):
    """
    Abstract base class defining the interface for JWT decode drivers.

    This interface specifies the contract for classes that handle JWT token decoding,
    providing methods to extract payloads from both bearer tokens and cookies.
    """

    @abc.abstractmethod
    def _get_payload(
        self,
        bearer_token: HTTPAuthorizationCredentials | None,
        cookie_token: str | None,
    ) -> Any:
        """Extract and verify the JWT payload from either bearer token or cookie.

        Args:
            bearer_token: The HTTP Authorization credentials containing the bearer token.
                         Expected to be in the format 'Bearer <token>'.
            cookie_token: The JWT token extracted from a cookie.

        Returns:
            The decoded JWT payload as a dictionary.

        Raises:
            HTTPException: If no valid token is provided or if token verification fails.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def _get_payload_optional(
        self,
        bearer_token: HTTPAuthorizationCredentials | None,
        cookie_token: str | None,
    ) -> Any | None:
        """Attempt to extract JWT payload without raising exceptions on failure.

        Args:
            bearer_token: The HTTP Authorization credentials containing the bearer token.
                         Expected to be in the format 'Bearer <token>'.
            cookie_token: The JWT token extracted from a cookie.

        Returns:
            The decoded JWT payload as a dictionary if successful, None otherwise.

        Note:
            This method differs from _get_payload by returning None instead of raising
            exceptions when token verification fails or no token is provided.
        """
        pass  # pragma: no cover


class IEncodeDriverJWT(metaclass=abc.ABCMeta):
    """Abstract base class defining the interface for JWT encoding operations.

    This interface specifies the contract for classes that handle JWT token generation,
    providing methods to create both access and refresh tokens either together or separately.
    """

    @abc.abstractmethod
    async def create_jwt_tokens(self, access_payload: BaseModel, refresh_payload: BaseModel) -> JWTTokensDTO:
        """Create both access and refresh tokens asynchronously.

        Args:
            access_payload: A Pydantic BaseModel containing the claims/data to be encoded
                           in the access token (typically user identity and permissions)
            refresh_payload: A Pydantic BaseModel containing the claims/data to be encoded
                           in the refresh token (typically just user identity for renewal)

        Returns:
            JWTTokensDTO: A data transfer object containing both the access_token
                        and refresh_token as strings

        Note:
            Implementations should handle proper signing and expiration times according
            to the configured JWT settings.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    async def create_access_token(self, access_payload: BaseModel) -> str:
        """Create only an access token asynchronously.

        Args:
            access_payload: A Pydantic BaseModel containing the claims/data to be encoded
                          in the access token

        Returns:
            str: The encoded JWT access token string

        Note:
            The token should be signed and include expiration as configured in JWT settings.
            Typically has a shorter lifespan than refresh tokens.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    async def create_refresh_token(self, refresh_payload: BaseModel) -> str:
        """Create only a refresh token asynchronously.

        Args:
            refresh_payload: A Pydantic BaseModel containing the claims/data to be encoded
                          in the refresh token

        Returns:
            str: The encoded JWT refresh token string

        Note:
            The token should be signed and include expiration as configured in JWT settings.
            Typically has a longer lifespan than access tokens and is used solely for
            obtaining new access tokens.
        """
        pass  # pragma: no cover


class BaseJWT(metaclass=abc.ABCMeta):
    __slots__ = (
        '_config',
        '_request',
        '_response',
    )

    def __init__(self) -> None:
        self._config: QuickJWTConfig | None = None
        self._request: Request | None = None
        self._response: Response | None = None

    def _setup_call_function_params(self, request: Request, response: Response) -> None:
        self._request = request
        self._response = response
        self._config = self._get_config_from_request()

    def _get_config_from_request(self) -> QuickJWTConfig:
        if self._request is None:
            raise AttributeError('_reqeust field not found')
        try:
            config: QuickJWTConfig = self._request.state.quick_jwt_config
            return config
        except AttributeError:
            raise Exception(
                """
                QuickJWTConfig not defined in middleware. Example of definition:'
                from fastapi import FastAPI
                from quick_jwt import QuickJWTConfig, QuickJWTMiddleware
                
                app = FastAPI()
                quick_jwt_config = QuickJWTConfig(encode_key='key', decode_key='key')
                app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
                """
            )

    def _get_config(self) -> QuickJWTConfig:
        if self._config is None:
            raise Exception('The __call__ function was not called.')
        return self._config

    def _get_request(self) -> Request:
        if self._request is None:
            raise Exception('The __call__ function was not called.')
        return self._request

    def _get_response(self) -> Response:
        if self._response is None:
            raise Exception('The __call__ function was not called.')
        return self._response
