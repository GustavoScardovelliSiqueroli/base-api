from fastapi import FastAPI

from arch_test.core.errors_handlers import domain_error_handler
from arch_test.core.exceptions import DomainException
from arch_test.modules.user.router import router as user_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_router)
    app.add_exception_handler(DomainException, domain_error_handler)  # type:ignore
    return app


app = create_app()
