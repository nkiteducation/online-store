from api.security.dependencies import verify_access_token
from api.security.endpoint import router as security
from api.products.endpoint import router as products
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/v1")
api = APIRouter(prefix="/api", dependencies=[Depends(verify_access_token)])

api.get("/health", status_code=status.HTTP_204_NO_CONTENT)(lambda: None)
api.include_router(products)

router.include_router(security)
router.include_router(api)
