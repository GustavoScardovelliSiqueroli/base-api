from fastapi import APIRouter

from arch_test.modules.auth.routers.v1.router import router as auth_router
from arch_test.modules.user.routers.v1.router import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
