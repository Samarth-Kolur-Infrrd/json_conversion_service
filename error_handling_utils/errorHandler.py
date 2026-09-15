from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def validation_exception_handler(
    request: Request,
    exc: ValidationError
):
    return JSONResponse(
        status_code=400,
        content={
            "status": "FAILURE",
            "error": exc.errors()[0]["msg"]
        }
    )