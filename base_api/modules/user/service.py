from typing import Iterable

from base_api.modules.user.models import User
from base_api.modules.user.repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def get_all_users(self) -> Iterable[User]:
        return self.user_repo.get_all()
