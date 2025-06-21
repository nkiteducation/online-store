from uuid import UUID

from api.security.utils import password_hash, verify_password
from database.models import User
from database.session import session_manager
from pydantic import EmailStr, SecretStr
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


@session_manager.connection
async def create_user(
    username: str,
    email: EmailStr,
    password: SecretStr,
    session: AsyncSession,
) -> None:
    hashed = password_hash(password.get_secret_value())
    stmt = insert(User).values(
        name=username,
        email=email,
        password=hashed,
    )
    await session.execute(stmt)
    await session.commit()


@session_manager.connection
async def email_exists(email: str, session: AsyncSession) -> bool:
    stmt = select(User.id).where(User.email == email)
    return await session.scalar(stmt) is not None


@session_manager.connection
async def username_exists(username: str, session: AsyncSession) -> bool:
    stmt = select(User.id).where(User.name == username)
    return await session.scalar(stmt) is not None


@session_manager.connection
async def get_user_by_id(
    id: int | UUID,
    session: AsyncSession,
) -> User | None:
    return await session.get(User, UUID(id))


@session_manager.connection
async def authenticate_user(
    username: str,
    password: str,
    session: AsyncSession,
) -> User | None:
    stmt = select(User).where(User.name == username)
    user = await session.scalar(stmt)
    if user and verify_password(password, user.password):
        return user
    return None
