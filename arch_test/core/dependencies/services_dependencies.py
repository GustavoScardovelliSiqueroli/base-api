from fastapi import Depends

from arch_test.core.dependencies.repositories_dependencies import get_user_repository
from arch_test.modules.user.repository import UserRepository
from arch_test.modules.user.service import UserService


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)
