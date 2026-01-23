from fastapi import Depends

from base_api.infra.db.repositories.inmemory_user_repository import (
    InMemoryUserRepository,
)
from base_api.modules.user.repository import UserRepository
from base_api.modules.user.service import UserService


def get_user_repository() -> UserRepository:
    return InMemoryUserRepository()


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)
