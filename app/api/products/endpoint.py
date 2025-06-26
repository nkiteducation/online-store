from uuid import UUID

from api.products.service import get_product_by_id, get_product_sorted
from api.products.shema import ProductsReturn, SortingProducts
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductsReturn])
async def get_list_products(sorting: SortingProducts = Depends()):
    return [
        ProductsReturn.model_validate(product, from_attributes=True)
        for product in await get_product_sorted(sorting)
    ]


@router.get("/{id}", response_model=ProductsReturn)
async def get_products(id: UUID):
    return ProductsReturn.model_validate(
        await get_product_by_id(id), from_attributes=True
    )
