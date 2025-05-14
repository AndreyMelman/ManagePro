from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.models import db_helper
from api import router as api_router
from errors_handlers import register_errors_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    title="ManagePro",
)

main_app.include_router(api_router)
register_errors_handlers(main_app)


@main_app.get("/")
async def root():
    return {"message": "Hello"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
