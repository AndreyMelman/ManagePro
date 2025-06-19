import logging

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
)

from core.config import settings
from core.models import Base, db_helper
from main import main_app

log = logging.getLogger(__name__)

DATABASE_URL = str(settings.db.url)

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture(scope="session", autouse=True)
def set_logging_level():
    logging.getLogger().setLevel(logging.WARNING)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    log.info("Creating database tables for test...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session():
    async with SessionFactory() as session:
        yield session


@pytest_asyncio.fixture(scope="function", autouse=True)
async def override_db_dependency():
    async def override_session_getter():
        async with SessionFactory() as session:
            yield session

    main_app.dependency_overrides[db_helper.session_getter] = override_session_getter
    yield
    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def user_data():
    return {"email": "test@example.com", "password": "12345678"}


@pytest_asyncio.fixture
async def user(client, user_data):
    resp = await client.post("/api/v1/users/", json=user_data)
    assert resp.status_code in (200, 201)
    return resp.json()


@pytest_asyncio.fixture
async def auth_headers(client, user_data):
    await client.post("/api/v1/users/", json=user_data)
    resp = await client.post("/api/v1/auth/jwt/login", data=user_data)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
