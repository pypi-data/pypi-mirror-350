from pydantic import BaseModel, Field


class JWTTokensDTO(BaseModel):
    access: str = Field(..., description='Access token string')
    refresh: str = Field(..., description='Refresh token string')
