from fastapi import FastAPI

from arch_test.modules.user.router import router as user_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_router)
    return app


app = create_app()
