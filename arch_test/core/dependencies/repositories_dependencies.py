from arch_test.infra.db.repositories.inmemory_user_repository import (
    InMemoryUserRepository,
)
from arch_test.modules.user.repository import UserRepository


def get_user_repository() -> UserRepository:
    return InMemoryUserRepository()
