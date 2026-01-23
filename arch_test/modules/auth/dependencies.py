from fastapi import Depends

from arch_test.modules.auth.service import AuthService
from arch_test.modules.user.dependencies import get_user_repository
from arch_test.modules.user.repository import UserRepository


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo=user_repo)
