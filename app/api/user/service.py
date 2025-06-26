# services/cart.py
from uuid import UUID

from database.models import Cart, Product, User
from database.session import session_manager
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


@session_manager.connection
async def get_user_cart_items(
    user_id: UUID,
    session: AsyncSession
) -> list[Cart]:
    result = await session.execute(
        select(Cart)
        .options(selectinload(Cart.product))
        .where(Cart.user_id == user_id)
    )
    return result.scalars().all()

@session_manager.connection
async def add_product_to_cart(
    user: User, product_id: UUID, quantity: int, session: AsyncSession
):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    result = await session.execute(
        select(Cart).where(
            Cart.user_id == user.id, Cart.product_id == product_id
        )
    )
    cart_item = result.scalars().first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(
            user_id=user.id, product_id=product_id, quantity=quantity
        )
        session.add(cart_item)

    await session.commit()
