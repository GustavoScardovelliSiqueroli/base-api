import uuid
from typing import Any, Iterable
from uuid import UUID

from arch_test.modules.user.model import User
from arch_test.modules.user.repository import UserRepository

users: list[User] = []


class InMemoryUser(UserRepository):
    def get_all(self) -> Iterable[User]:
        return users

    def get_by_id(self, id: UUID):
        for user in users:
            if user.user_id == id:
                return user

    def create(self, data: User) -> User:
        data.user_id = uuid.uuid4().hex
        users.append(data)
        return data

    def update(self, data: dict[str, Any]) -> User: ...
    def delete(self) -> None: ...
