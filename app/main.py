from contextlib import asynccontextmanager

import uvicorn
from api import router
from core.config import settings
from core.logger import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    yield
    logger.info("Shutting down application...")


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)

app.include_router(router)

app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        workers=settings.api.workers,
        reload=settings.development,
    )
