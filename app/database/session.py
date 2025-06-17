import asyncio
from functools import wraps

from core.config import settings
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


class SessionManager:
    def __init__(self, database_url: str, **engine_kwargs: dict) -> None:
        self.engine = create_async_engine(
            database_url,
            future=True,
            **engine_kwargs,
        )
        self.session_local = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )
        self.scoped_session = async_scoped_session(
            self.session_local,
            scopefunc=asyncio.current_task,
        )

    def connection(self, method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with self.session_local() as session:
                return await method(*args, session=session, **kwargs)

        return wrapper

    async def dispose(self) -> None:
        await self.engine.dispose()


session_manager = SessionManager(
    database_url=settings.database.url.get(),
    pool_size=settings.database.poolSize,
    max_overflow=settings.database.maxOverflow,
    pool_timeout=settings.database.poolTimeout,
)
