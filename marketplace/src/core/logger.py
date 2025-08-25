from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse


def setup_exception_handlers(app: FastAPI) -> None:
    logger.remove()
    logger.add(
        "errors.log",
        rotation="10 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="ERROR",
    )

    logger.add(
        "debug.log",
        rotation="10 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG",
        filter=lambda record: record["level"].name not in ["ERROR", "CRITICAL"]
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(
            f"Unhandled exception: {exc}\n"
            f"Request: {request.method} {request.url}\n"
            f"Headers: {dict(request.headers)}"
        )

        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )
