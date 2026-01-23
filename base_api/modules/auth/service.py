import bcrypt

from base_api.modules.auth.schemas import RegisterUserSchema
from base_api.modules.user.models import User
from base_api.modules.user.repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def login(self): ...

    def register(self, data: RegisterUserSchema) -> User:
        user = User(login=data.login, password=self._hash_password(data.password))
        return self.user_repo.create(user)

    def _hash_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password.decode("utf-8")
