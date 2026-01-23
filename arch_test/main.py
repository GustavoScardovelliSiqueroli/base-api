from fastapi import FastAPI

from arch_test.api.v1.router import router as router_v1
from arch_test.core.errors_handlers import domain_error_handler
from arch_test.core.exceptions import DomainException


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router_v1, prefix="/api/v1")
    app.add_exception_handler(DomainException, domain_error_handler)  # type:ignore
    return app


app = create_app()
