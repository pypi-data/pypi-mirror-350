import json
import typing
from datetime import timedelta
from typing import Any, TypedDict, Iterable, Sequence


class ModelValidateKwargs(TypedDict, total=False):
    strict: bool | None
    from_attributes: bool | None
    context: Any | None
    by_alias: bool | None
    by_name: bool | None


class JWTEncodeKwargs(TypedDict, total=False):
    key: str | bytes
    algorithm: str | None
    headers: dict[str, Any] | None
    json_encoder: type[json.JSONEncoder] | None
    sort_headers: bool


class JWTDecodeKwargs(TypedDict, total=False):
    key: str | bytes
    algorithms: Sequence[str] | None
    options: dict[str, Any] | None
    verify: bool | None
    detached_payload: bytes | None
    audience: str | Iterable[str] | None
    subject: str | None
    issuer: str | Sequence[str] | None
    leeway: float | timedelta


class SetCookieKwargs(TypedDict, total=False):
    key: str
    max_age: int | None
    path: str | None
    domain: str | None
    secure: bool
    httponly: bool
    samesite: typing.Literal['lax', 'strict', 'none'] | None
