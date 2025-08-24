from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from src.core.database import db_helper
from src.core.config import settings
from src.auth import auth_router
from src.core.fs_broker import broker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await broker.start()
    yield
    await db_helper.dispose()
    await broker.stop()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(auth_router, prefix=settings.api.api_prefix)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:main_app",
        host=settings.run.host,
        port=8000,
        reload=settings.run.reload,
        workers=settings.run.workers,
    )
