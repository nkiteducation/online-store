from decimal import Decimal
from uuid import UUID

from api.products.shema import SortingProducts
from database.models import Product
from database.session import session_manager
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


@session_manager.connection
async def get_product_sorted(
    sorting: SortingProducts, session: AsyncSession
) -> list[Product]:
    stmt = select(Product).order_by(Product.price.asc())

    if sorting.name:
        stmt = stmt.where(Product.name.ilike(f"%{sorting.name}%"))
    if sorting.min_price:
        stmt = stmt.where(Product.price >= sorting.min_price)
    if sorting.max_price:
        stmt = stmt.where(Product.price <= sorting.max_price)
    if sorting.skip:
        stmt = stmt.offset(sorting.skip)
    if sorting.limit:
        stmt = stmt.limit(sorting.limit)

    result = await session.execute(stmt)
    return result.scalars().all()


@session_manager.connection
async def get_product_by_id(id: UUID, session: AsyncSession):
    return await session.get(Product, id)


@session_manager.connection
async def add_products(
    name: str, description: str, price: Decimal, session: AsyncSession
) -> UUID:
    stmt = (
        insert(Product)
        .values(name=name, description=description, price=price)
        .returning(Product.id)
    )
    id = await session.execute(stmt)
    await session.commit()
    return id


@session_manager.connection
async def upgrade_products(id: UUID, session: AsyncSession, **kwargs) -> UUID:
    stmt = (
        update(Product)
        .where(Product.id == id)
        .values(kwargs)
        .returning(Product.id)
    )
    id = await session.execute(stmt)
    await session.commit()
    return id


@session_manager.connection
async def delete_products(id: UUID, session: AsyncSession):
    stmt = delete(Product).where(Product.id == id)
    await session.execute(stmt)
    await session.commit()
