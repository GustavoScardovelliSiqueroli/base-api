from typing import Iterable

from arch_test.modules.user.model import User
from arch_test.modules.user.repository import UserRepository
from arch_test.modules.user.schemas import CreateUserSchema


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def create_user(self, data: CreateUserSchema) -> User:
        user = User(login=data.login, password=data.password)
        return self.user_repo.create(user)

    def get_all_users(self) -> Iterable[User]:
        return self.user_repo.get_all()
