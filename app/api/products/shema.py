from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, Field


class Products(BaseModel):
    name: str
    description: str
    price: Annotated[
        Decimal, Field(ge=Decimal("0.00"), max_digits=10, decimal_places=2)
    ]


class ProductsUpdete(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Annotated[
        Optional[Decimal],
        Field(ge=Decimal("0.00"), max_digits=10, decimal_places=2),
    ] = None


class ProductsReturn(Products):
    id: UUID
    created_at: datetime
    updated_at: datetime


class SortingProducts(BaseModel):
    name: Annotated[Optional[str], Query()] = None
    skip: Annotated[Optional[int], Query(ge=0)] = None
    limit: Annotated[Optional[int], Query(ge=0)] = None
    min_price: Annotated[
        Optional[Decimal],
        Query(ge=Decimal("0.00"), max_digits=10, decimal_places=2),
    ] = None
    max_price: Annotated[
        Optional[Decimal],
        Query(ge=Decimal("0.00"), max_digits=10, decimal_places=2),
    ] = None
