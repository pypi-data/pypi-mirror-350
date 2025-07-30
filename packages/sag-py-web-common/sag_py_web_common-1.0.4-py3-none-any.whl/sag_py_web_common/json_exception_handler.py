import logging
from logging import Logger
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

logger: Logger = logging.getLogger("http_error_logger")


async def handle_unknown_exception(_: Any, exception: Exception) -> JSONResponse:
    """Per default fastapi just returns the exception text. We want to return a json instead for rest apis.

    Returns:
        JSONResponse: A json response that contains the field 'detail' with the exception message.
    """
    logger.error("An unknown Error!", exc_info=True, extra={"response_status": 500})
    return JSONResponse(status_code=500, content=jsonable_encoder({"detail": str(exception)}))


async def log_exception(_, exception: StarletteHTTPException) -> Response:  # type: ignore
    logger.error("An HTTP Error! %s", exception.detail, extra={"response_status": exception.status_code})

    return await http_exception_handler(_, exception)
