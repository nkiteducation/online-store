from uuid import UUID

from api.products.shema import ProductsReturn
from pydantic import BaseModel


class CartItemCreate(BaseModel):
    id: UUID
    quantity: int = 1


class CartItemReturn(BaseModel):
    product: ProductsReturn
    quantity: int
