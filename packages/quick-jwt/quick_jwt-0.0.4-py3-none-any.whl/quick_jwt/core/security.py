from typing import Annotated

from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

access_bearer_security = Annotated[
    HTTPAuthorizationCredentials | None,
    Security(
        HTTPBearer(
            bearerFormat='Bearer',
            scheme_name='JWT access token into headers',
            description='The input value is inserted as follows: "Authorization: Bearer {value}"',
            auto_error=False,
        )
    ),
]

refresh_bearer_security = Annotated[
    HTTPAuthorizationCredentials | None,
    Security(
        HTTPBearer(
            bearerFormat='Bearer',
            scheme_name='JWT refresh token into headers',
            description='The input value is inserted as follows: "Authorization: Bearer {value}"',
            auto_error=False,
        )
    ),
]
