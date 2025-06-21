from pydantic import BaseModel, EmailStr, SecretStr


class SecuritySchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
