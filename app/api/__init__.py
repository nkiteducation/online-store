from api.security.endpoint import router as security
from api.products.endpoint import router as products
from api.admin.endpoint import router as admin
from api.security.dependencies import htttp_bearer
from fastapi import Depends
from fastapi import APIRouter, status

router = APIRouter(prefix="/v1")

router.get("/health", status_code=status.HTTP_204_NO_CONTENT)(lambda: None)

router.include_router(security)
router.include_router(products)
router.include_router(admin, dependencies=[Depends(htttp_bearer)])
