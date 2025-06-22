from api.security.dependencies import verify_access_token
from api.security.endpoint import router as security
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/v1")
api = APIRouter(prefix="/api", dependencies=[Depends(verify_access_token)])

api.get("/health", status_code=status.HTTP_204_NO_CONTENT)(lambda: None)

router.include_router(security)
router.include_router(api)
