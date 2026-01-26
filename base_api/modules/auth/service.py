from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from base_api.core.configs import Settings
from base_api.core.exceptions import AuthenticationError
from base_api.modules.auth.schemas import LoginUserSchema, RegisterUserSchema
from base_api.modules.user.models import User
from base_api.modules.user.repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository, settings: Settings) -> None:
        self.user_repo = user_repo
        self.settings = settings

    async def login(self, data: LoginUserSchema) -> str:
        user = await self.user_repo.get_by_login(data.login)

        if not user or not self._validate_password(data.password, user.password):
            raise AuthenticationError()

        return self._generate_jwt(user)

    async def register(self, data: RegisterUserSchema) -> User:
        user = User(login=data.login, password=self._hash_password(data.password))
        return await self.user_repo.create(user)

    def _hash_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def _validate_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), hashed_password.encode('utf-8')
        )

    def _generate_jwt(self, user: User) -> str:
        now = datetime.now(tz=timezone.utc)
        expire = now + timedelta(hours=self.settings.ACCESS_TOKEN_EXPIRE_HOURS)
        payload = {
            'sub': str(user.user_id),
            'exp': int(expire.timestamp()),
            'iat': int(now.timestamp()),
        }
        token = jwt.encode(
            payload, self.settings.API_KEY, algorithm=self.settings.JWT_ALGORITHM
        )  # type: ignore
        return token
