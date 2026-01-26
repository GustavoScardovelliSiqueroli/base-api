from fastapi import Depends

from base_api.core.configs import Settings, get_settings
from base_api.modules.auth.service import AuthService
from base_api.modules.user.dependencies import get_user_repository
from base_api.modules.user.repository import UserRepository


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    return AuthService(user_repo=user_repo, settings=settings)
