from uuid import UUID

from api.products.service import (
    add_products,
    delete_products,
    upgrade_products,
)
from api.products.shema import Products, ProductsUpdete
from api.security.dependencies import ROLE_SCOPES, validate_scopes
from fastapi import APIRouter, Security, status

router = APIRouter(
    prefix="/admins",
    tags=["Admin"],
    dependencies=[Security(validate_scopes, scopes=ROLE_SCOPES["admin"])],
)


@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_products(data: Products):
    ID = await add_products(**data.model_dump())
    return {"ID": ID}


@router.patch("/products/{id}", status_code=status.HTTP_200_OK)
async def update_product(id: UUID, data: ProductsUpdete):
    ID = await upgrade_products(id, **data.model_dump(exclude_none=True))
    return {"ID": ID}


@router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: UUID):
    await delete_products(id)
