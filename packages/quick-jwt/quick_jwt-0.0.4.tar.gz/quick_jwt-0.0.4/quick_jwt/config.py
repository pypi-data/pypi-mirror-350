import json
import typing
from datetime import timedelta
from typing import Any, Sequence, Iterable, Annotated
from typing_extensions import Doc

from fastapi import HTTPException, status
from jwt import PyJWT
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from quick_jwt.core._function_args import (
    JWTDecodeKwargs,
    JWTEncodeKwargs,
    SetCookieKwargs,
)


class QuickJWTConfig(BaseSettings):
    """Configuration class for QuickJWT settings.

    Attributes:
        encode_key: Key used for encoding JWT tokens (required)
        decode_key: Key used for decoding JWT tokens (required)
        driver: JWT library driver instance (default: PyJWT())

        access_token_name: Name of the access token cookie (default: 'access')
        access_token_expires: Expiration time for access tokens (default: 2 days)
        access_token_path: Cookie path for access token (default: '/')
        access_token_domain: Cookie domain for access token (default: None)
        access_token_secure: Secure flag for access token cookie (default: False)
        access_token_httponly: HttpOnly flag for access token cookie (default: False)
        access_token_samesite: SameSite policy for access token cookie (default: 'lax')

        refresh_token_name: Name of the refresh token cookie (default: 'refresh')
        refresh_token_expires: Expiration time for refresh tokens (default: 2 weeks)
        refresh_token_path: Cookie path for refresh token (default: '/')
        refresh_token_domain: Cookie domain for refresh token (default: None)
        refresh_token_secure: Secure flag for refresh token cookie (default: False)
        refresh_token_httponly: HttpOnly flag for refresh token cookie (default: False)
        refresh_token_samesite: SameSite policy for refresh token cookie (default: 'lax')

        encode_algorithm: Algorithm used for encoding tokens (default: 'HS256')
        encode_headers: Additional headers to include in encoded tokens (default: None)
        encode_json_encoder: Custom JSON encoder for token payload (default: None)
        encode_sort_headers: Whether to sort headers when encoding (default: True)

        decode_algorithms: List of allowed algorithms for decoding (default: ['HS256'])
        decode_options: Dictionary of decoding options (default: None)
        decode_verify: Whether to verify the token when decoding (default: None)
        decode_detached_payload: Detached payload for decoding (default: None)
        decode_audience: Expected audience value(s) for verification (default: None)
        decode_subject: Expected subject for verification (default: None)
        decode_issuer: Expected issuer for verification (default: None)
        decode_leeway: Leeway time for expiration verification (default: 0)
    """

    model_config = SettingsConfigDict()

    driver: PyJWT | Any = Field(PyJWT())

    encode_key: str | bytes = Field(...)
    decode_key: str | bytes = Field(...)

    access_token_name: str = Field('access')
    access_token_expires: timedelta = Field(timedelta(days=2))
    access_token_path: str | None = Field('/')
    access_token_domain: str | None = Field(None)
    access_token_secure: bool = Field(False)
    access_token_httponly: bool = Field(False)
    access_token_samesite: typing.Literal['lax', 'strict', 'none'] | None = Field('lax')

    refresh_token_name: str = Field('refresh')
    refresh_token_expires: timedelta = Field(timedelta(weeks=2))
    refresh_token_path: str | None = Field('/')
    refresh_token_domain: str | None = Field(None)
    refresh_token_secure: bool = Field(False)
    refresh_token_httponly: bool = Field(False)
    refresh_token_samesite: typing.Literal['lax', 'strict', 'none'] | None = Field('lax')

    encode_algorithm: str | None = Field('HS256')
    encode_headers: dict[str, Any] | None = Field(None)
    encode_json_encoder: type[json.JSONEncoder] | None = Field(None)
    encode_sort_headers: bool = Field(True)

    decode_algorithms: Sequence[str] | None = Field(['HS256'])
    decode_options: dict[str, Any] | None = Field(None)
    decode_verify: bool | None = Field(None)
    decode_detached_payload: bytes | None = Field(None)
    decode_audience: str | Iterable[str] | None = Field(None)
    decode_subject: str | None = Field(None)
    decode_issuer: str | Sequence[str] | None = Field(None)
    decode_leeway: float | timedelta = Field(0)

    def __init__(
        self,
        encode_key: Annotated[
            str | bytes,
            Doc(
                """
                    Key used for encoding JWT tokens (required)
                    """
            ),
        ],
        decode_key: Annotated[
            str | bytes,
            Doc(
                """
                    Key used for decoding JWT tokens (required)
                    """
            ),
        ],
        driver: Annotated[
            PyJWT | Any,
            Doc(
                """
                    JWT library driver instance
                    Default: PyJWT()
                    """
            ),
        ] = PyJWT(),
        access_token_name: Annotated[
            str,
            Doc(
                """
                    Name of the access token cookie
                    Default: 'access'
                    """
            ),
        ] = 'access',
        access_token_expires: Annotated[
            timedelta,
            Doc(
                """
                    Expiration time for access tokens
                    Default: 2 days
                    """
            ),
        ] = timedelta(days=2),
        access_token_path: Annotated[
            str | None,
            Doc(
                """
                    Cookie path for access token
                    Default: '/'
                    """
            ),
        ] = '/',
        access_token_domain: Annotated[
            str | None,
            Doc(
                """
                    Cookie domain for access token
                    Default: None
                    """
            ),
        ] = None,
        access_token_secure: Annotated[
            bool,
            Doc(
                """
                    Secure flag for access token cookie
                    Default: False
                    """
            ),
        ] = False,
        access_token_httponly: Annotated[
            bool,
            Doc(
                """
                    HttpOnly flag for access token cookie
                    Default: False
                    """
            ),
        ] = False,
        access_token_samesite: Annotated[
            typing.Literal['lax', 'strict', 'none'] | None,
            Doc(
                """
                    SameSite policy for access token cookie
                    Default: 'lax'
                    """
            ),
        ] = 'lax',
        refresh_token_name: Annotated[
            str,
            Doc(
                """
                    Name of the refresh token cookie
                    Default: 'refresh'
                    """
            ),
        ] = 'refresh',
        refresh_token_expires: Annotated[
            timedelta,
            Doc(
                """
                    Expiration time for refresh tokens
                    Default: 2 weeks
                    """
            ),
        ] = timedelta(weeks=2),
        refresh_token_path: Annotated[
            str | None,
            Doc(
                """
                    Cookie path for refresh token
                    Default: '/'
                    """
            ),
        ] = '/',
        refresh_token_domain: Annotated[
            str | None,
            Doc(
                """
                    Cookie domain for refresh token
                    Default: None
                    """
            ),
        ] = None,
        refresh_token_secure: Annotated[
            bool,
            Doc(
                """
                    Secure flag for refresh token cookie
                    Default: False
                    """
            ),
        ] = False,
        refresh_token_httponly: Annotated[
            bool,
            Doc(
                """
                    HttpOnly flag for refresh token cookie
                    Default: False
                    """
            ),
        ] = False,
        refresh_token_samesite: Annotated[
            typing.Literal['lax', 'strict', 'none'] | None,
            Doc(
                """
                    SameSite policy for refresh token cookie
                    Default: 'lax'
                    """
            ),
        ] = 'lax',
        encode_algorithm: Annotated[
            str | None,
            Doc(
                """
                    Algorithm used for encoding tokens
                    Default: 'HS256'
                    """
            ),
        ] = 'HS256',
        encode_headers: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                    Additional headers to include in encoded tokens
                    Default: None
                    """
            ),
        ] = None,
        encode_json_encoder: Annotated[
            type[json.JSONEncoder] | None,
            Doc(
                """
                    Custom JSON encoder for token payload
                    Default: None
                    """
            ),
        ] = None,
        encode_sort_headers: Annotated[
            bool,
            Doc(
                """
                    Whether to sort headers when encoding
                    Default: True
                    """
            ),
        ] = True,
        decode_algorithms: Annotated[
            Sequence[str] | None,
            Doc(
                """
                    List of allowed algorithms for decoding
                    Default: ['HS256']
                    """
            ),
        ] = ('HS256',),
        decode_options: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                    Dictionary of decoding options
                    Default: None
                    """
            ),
        ] = None,
        decode_verify: Annotated[
            bool | None,
            Doc(
                """
                    Whether to verify the token when decoding
                    Default: None
                    """
            ),
        ] = None,
        decode_detached_payload: Annotated[
            bytes | None,
            Doc(
                """
                    Detached payload for decoding
                    Default: None
                    """
            ),
        ] = None,
        decode_audience: Annotated[
            str | Iterable[str] | None,
            Doc(
                """
                    Expected audience value(s) for verification
                    Default: None
                    """
            ),
        ] = None,
        decode_subject: Annotated[
            str | None,
            Doc(
                """
                    Expected subject for verification
                    Default: None
                    """
            ),
        ] = None,
        decode_issuer: Annotated[
            str | Sequence[str] | None,
            Doc(
                """
                    Expected issuer for verification
                    Default: None
                    """
            ),
        ] = None,
        decode_leeway: Annotated[
            float | timedelta,
            Doc(
                """
                    Leeway time for expiration verification
                    Default: 0
                    """
            ),
        ] = 0,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            driver=driver,
            encode_key=encode_key,
            decode_key=decode_key,
            access_token_name=access_token_name,
            access_token_expires=access_token_expires,
            access_token_path=access_token_path,
            access_token_domain=access_token_domain,
            access_token_secure=access_token_secure,
            access_token_httponly=access_token_httponly,
            access_token_samesite=access_token_samesite,
            refresh_token_name=refresh_token_name,
            refresh_token_expires=refresh_token_expires,
            refresh_token_path=refresh_token_path,
            refresh_token_domain=refresh_token_domain,
            refresh_token_secure=refresh_token_secure,
            refresh_token_httponly=refresh_token_httponly,
            refresh_token_samesite=refresh_token_samesite,
            encode_algorithm=encode_algorithm,
            encode_headers=encode_headers,
            encode_json_encoder=encode_json_encoder,
            encode_sort_headers=encode_sort_headers,
            decode_algorithms=decode_algorithms,
            decode_options=decode_options,
            decode_verify=decode_verify,
            decode_detached_payload=decode_detached_payload,
            decode_audience=decode_audience,
            decode_subject=decode_subject,
            decode_issuer=decode_issuer,
            decode_leeway=decode_leeway,
            **kwargs,
        )

    def build_encode_params(self) -> JWTEncodeKwargs:
        return {
            'key': self.encode_key,
            'algorithm': self.encode_algorithm,
            'headers': self.encode_headers,
            'json_encoder': self.encode_json_encoder,
            'sort_headers': self.encode_sort_headers,
        }

    def build_decode_params(self) -> JWTDecodeKwargs:
        return {
            'key': self.decode_key,
            'algorithms': self.decode_algorithms,
            'options': self.decode_options,
            'verify': self.decode_verify,
            'detached_payload': self.decode_detached_payload,
            'audience': self.decode_audience,
            'subject': self.decode_subject,
            'issuer': self.decode_issuer,
            'leeway': self.decode_leeway,
        }

    def build_access_token_params(self) -> SetCookieKwargs:
        return {
            'key': self.access_token_name,
            'max_age': int(self.access_token_expires.total_seconds()),
            'path': self.access_token_path,
            'domain': self.access_token_domain,
            'secure': self.access_token_secure,
            'httponly': self.access_token_httponly,
            'samesite': self.access_token_samesite,
        }

    def build_refresh_token_params(self) -> SetCookieKwargs:
        return {
            'key': self.refresh_token_name,
            'max_age': int(self.refresh_token_expires.total_seconds()),
            'path': self.refresh_token_path,
            'domain': self.refresh_token_domain,
            'secure': self.refresh_token_secure,
            'httponly': self.refresh_token_httponly,
            'samesite': self.refresh_token_samesite,
        }

    def build_unauthorized_http_exception(self) -> HTTPException:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
