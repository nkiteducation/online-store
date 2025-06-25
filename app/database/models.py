import enum
from decimal import Decimal
from uuid import UUID

from database.mixin import TimestampMixin, UUIDMixin
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, MetaData, Numeric
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
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

    cart_items: Mapped[list["Cart"]] = relationship(
        "Cart",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Product(CoreModel, UUIDMixin, TimestampMixin):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    in_carts: Mapped[list["Cart"]] = relationship(
        "Cart",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class Cart(CoreModel, UUIDMixin, TimestampMixin):
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="cart_items",
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="in_carts",
    )
