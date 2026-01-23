from fastapi import FastAPI

from base_api.api.v1.router import router as router_v1
from base_api.core.errors_handlers import domain_error_handler
from base_api.core.exceptions import DomainException


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router_v1, prefix="/api/v1")
    app.add_exception_handler(DomainException, domain_error_handler)  # type:ignore
    return app


app = create_app()
