from api.security.service import authenticate_user as _authenticate_user
from api.security.service import get_user_by_id
from api.security.utils import decode_jwt
from database.models import User
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt import InvalidTokenError

ALL_SCOPES = {
    "products:read": "View products",
    "products:write": "Modify products",
    "users:read": "View user profiles",
    "users:write": "Edit user profiles",
    "cart:read": "View your cart",
    "cart:write": "Edit your cart",
    "orders:read": "View your orders",
    "orders:write": "Place orders",
    "orders:manage": "Manage all orders",
    "payments:process": "Process payments",
    "refunds:issue": "Issue refunds",
    "admin:*": "All administrative actions",
}

ROLE_SCOPES = {
    "admin": list(ALL_SCOPES.keys()),
    "user": [
        "products:read",
        "cart:read",
        "cart:write",
        "orders:read",
        "orders:write",
        "payments:process",
    ],
    "ghost": [
        "products:read",
    ],
}


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/v1/security/token",
    scopes=ALL_SCOPES,
)


def _raise_auth_error(
    status_code: int,
    detail: str,
    www_authenticate: bool = False,
) -> None:
    headers = {"WWW-Authenticate": "Bearer"} if www_authenticate else None
    raise HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers,
    )


def _decode_token(
    token: str,
    type: str,
) -> dict:
    try:
        payload = decode_jwt(token)
        if payload["type"] != type:
            _raise_auth_error(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid token type",
                www_authenticate=True,
            )
        return payload
    except InvalidTokenError:
        _raise_auth_error(
            status.HTTP_401_UNAUTHORIZED,
            f"Invalid or expired {type} token",
            www_authenticate=True,
        )


async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await _authenticate_user(form_data.username, form_data.password)
    if not user:
        _raise_auth_error(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid username or password",
            www_authenticate=True,
        )
    return user


def verify_refresh_token(
    refresh: str | None = Cookie(
        alias="refresh-token",
        include_in_schema=False,
    ),
) -> dict:
    return _decode_token(
        refresh,
        type="refresh",
    )


def verify_access_token(
    token: str = Depends(oauth2_scheme),
) -> dict:
    return _decode_token(
        token,
        type="access",
    )


async def get_current_user(
    security_scopes: SecurityScopes,
    payload: dict = Depends(verify_access_token),
) -> User:
    token_scopes = payload.get("scopes", [])
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough rights",
                headers={
                    "WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'
                },
            )

    if user := await get_user_by_id(payload.get("sub")):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"user ID:{payload.get('sub')} not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
