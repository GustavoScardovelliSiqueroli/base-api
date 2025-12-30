from arch_test.infra.db.repositories.inmemory_user import InMemoryUser
from arch_test.modules.user.repository import UserRepository


def get_user_repository() -> UserRepository:
    return InMemoryUser()
