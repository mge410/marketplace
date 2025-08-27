from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from src.auth import auth_router
from src.posts import categories_router, posts_router
from src.core.config import settings
from src.core.database import db_helper
from src.core.fast_stream.fs_broker import broker
from src.core.fast_stream.fs_subs import router as subs_router
from src.core.logger import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await broker.start()
    yield
    await db_helper.dispose()
    await broker.stop()


main_app = FastAPI(
    lifespan=lifespan,
)
setup_exception_handlers(main_app)

broker.include_router(subs_router)

main_app.include_router(auth_router, prefix=settings.api.api_prefix)
main_app.include_router(categories_router, prefix=settings.api.api_prefix)
main_app.include_router(posts_router, prefix=settings.api.api_prefix)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:main_app",
        host=settings.run.host,
        port=8000,
        reload=settings.run.reload,
        workers=settings.run.workers,
    )
