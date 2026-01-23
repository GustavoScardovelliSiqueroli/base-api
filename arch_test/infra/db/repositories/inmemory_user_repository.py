import uuid
from typing import Any, Iterable
from uuid import UUID

from arch_test.core.exceptions import DuplicatedError
from arch_test.modules.user.model import User
from arch_test.modules.user.repository import UserRepository

users: list[User] = []


class InMemoryUserRepository(UserRepository):
    def get_all(self) -> Iterable[User]:
        return users

    def get_by_id(self, id: UUID):
        for user in users:
            if user.user_id == id:
                return user

    def create(self, data: User) -> User:
        for user in users:
            if user.login == data.login:
                raise DuplicatedError("login")

        if not data.user_id:
            data.user_id = uuid.uuid4()

        users.append(data)
        return data

    def update(self, data: dict[str, Any]) -> User: ...
    def delete(self) -> None: ...
