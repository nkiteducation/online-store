from api.security.dependencies import (
    ROLE_SCOPES,
    get_current_user,
    validate_scopes,
)
from api.user.service import add_product_to_cart, get_user_cart_items
from api.user.shema import CartItemReturn, CartItemCreate
from database.models import User
from fastapi import APIRouter, Depends, Security, status

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Security(validate_scopes, scopes=ROLE_SCOPES["user"])],
)


@router.post("/cart", status_code=status.HTTP_201_CREATED)
async def add_cart(
    item: CartItemCreate, user: User = Depends(get_current_user)
):
    await add_product_to_cart(user, item.id, item.quantity)


@router.get(
    "/cart",
    status_code=status.HTTP_200_OK,
    response_model=list[CartItemReturn],
)
async def get_cart(
    user: User = Depends(get_current_user),
):
    return [
        CartItemReturn.model_validate(item, from_attributes=True)
        for item in await get_user_cart_items(user.id)
    ]
