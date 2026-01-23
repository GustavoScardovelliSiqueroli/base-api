from fastapi import APIRouter

from base_api.modules.auth.routers.v1.router import router as auth_router
from base_api.modules.user.routers.v1.router import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
