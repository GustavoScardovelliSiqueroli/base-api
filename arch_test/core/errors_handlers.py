from fastapi import Request
from fastapi.responses import JSONResponse

from arch_test.core.exceptions import DomainException


def domain_error_handler(_: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.http_status_code,
        content={
            "success": False,
            "error": {"code": exc.internal_code.value, "message": exc.message},
        },
    )
