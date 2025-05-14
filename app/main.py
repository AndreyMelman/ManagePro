import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.models import db_helper
from api import router as api_router
from create_fastapi_app import create_app

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()


main_app = create_app()

main_app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
