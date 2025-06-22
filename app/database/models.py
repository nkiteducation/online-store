from decimal import Decimal
import enum

from database.mixin import TimestampMixin, UUIDMixin
from sqlalchemy import Enum as SQLEnum, Numeric
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

metadata = MetaData(
    naming_convention={
        "pk": "pk_%(table_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "ix": "ix_%(table_name)s_%(column_0_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
    },
)


class CoreModel(DeclarativeBase, AsyncAttrs):
    metadata = metadata

    @declared_attr
    def __tablename__(self) -> str:
        return "".join(
            ["_" + c.lower() if c.isupper() else c for c in self.__name__],
        ).lstrip("_")


class Role(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GHOST = "ghost"


class User(CoreModel, UUIDMixin, TimestampMixin):
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, name="enum_user_role"),
        default=Role.USER,
    )


class Product(CoreModel, UUIDMixin, TimestampMixin):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
