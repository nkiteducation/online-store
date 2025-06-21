import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from core.config import settings

_PRIVATE_KEY = settings.jwt.private_key_path.read_text()
_PUBLIC_KEY = settings.jwt.public_key_path.read_text()
TOKEN_TYPE_FIELD = "type"
ACCESS_TYPE = "access"
REFRESH_TYPE = "refresh"


def password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


def encode_jwt(payload: dict, expire_delta: timedelta) -> str:
    now = datetime.now(UTC)
    to_encode = {
        **payload,
        "iat": now,
        "exp": now + expire_delta,
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(to_encode, key=_PRIVATE_KEY, algorithm="RS256")


def decode_jwt(token: str) -> dict:
    return jwt.decode(
        jwt=token,
        key=_PUBLIC_KEY,
        algorithms=["RS256"],
    )


def jwt_factory(
    token_type: str,
    lifetime: timedelta,
) -> Callable[[dict[str, any]], str]:
    def create_token(payload: dict[str, any]) -> str:
        data = payload.copy()
        data[TOKEN_TYPE_FIELD] = token_type
        return encode_jwt(data, lifetime)

    return create_token


create_access_token = jwt_factory(
    ACCESS_TYPE,
    settings.jwt.access_token_lifetime,
)
create_refresh_token = jwt_factory(
    REFRESH_TYPE,
    settings.jwt.refresh_token_lifetime,
)
