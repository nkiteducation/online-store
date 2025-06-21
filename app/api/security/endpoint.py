from typing import Annotated

from api.security.dependencies import (
    ROLE_SCOPES,
    authenticate_user,
    verify_refresh_token,
)
from api.security.service import create_user as register_in_db
from api.security.service import email_exists, username_exists
from api.security.shema import SecuritySchema, TokenResponse
from api.security.utils import create_access_token, create_refresh_token
from core.config import settings
from database.models import User
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/security", tags=["Security"])


async def _ensure_unique_username_email(username: str, email: str) -> None:
    if await username_exists(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    if await email_exists(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data: SecuritySchema):
    await _ensure_unique_username_email(data.username, data.email)
    await register_in_db(**data.model_dump())
    return {"status": "OK"}


@router.post("/token", response_model=TokenResponse)
def login_user(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user: Annotated[User, Depends(authenticate_user)],
):
    scopes = ROLE_SCOPES.get(user.role.value, [])

    if form_data.scopes:
        allowed_scopes = set(scopes)
        requested_set = set(form_data.scopes)
        scopes = list(requested_set & allowed_scopes)
        if not scopes:
            scopes = list(allowed_scopes)

    refresh_token = create_refresh_token(
        {
            "sub": str(user.id),
            "scopes": scopes,
        },
    )
    access_token = create_access_token(
        {
            "sub": str(user.id),
            "scopes": scopes,
        },
    )

    response.set_cookie(
        key="refresh-token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/v1/security",
        max_age=settings.jwt.refresh_token_lifetime,
    )
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    payload: Annotated[dict, Depends(verify_refresh_token)],
):
    new_access = create_access_token(
        {
            "sub": payload.get("sub"),
            "scopes": payload.get("scopes"),
        },
    )
    return TokenResponse(access_token=new_access)
