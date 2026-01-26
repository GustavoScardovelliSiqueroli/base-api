import uuid
from typing import Any, Iterable
from uuid import UUID

from base_api.core.exceptions import DuplicatedError
from base_api.modules.user.models import User
from base_api.modules.user.repository import UserRepository

users: list[User] = []


class InMemoryUserRepository(UserRepository):
    async def get_all(self) -> Iterable[User]:
        return users

    async def get_by_id(self, id: UUID) -> User | None:
        for user in users:
            if user.user_id == id:
                return user

    async def get_by_login(self, login: str) -> User | None:
        for user in users:
            if user.login == login:
                return user

    async def create(self, data: User) -> User:
        for user in users:
            if user.login == data.login:
                raise DuplicatedError('login')

        if not data.user_id:
            data.user_id = uuid.uuid4()

        users.append(data)
        return data

    async def update(self, data: dict[str, Any]) -> User: ...
    async def delete(self) -> None: ...
