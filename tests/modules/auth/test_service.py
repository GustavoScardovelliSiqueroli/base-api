from unittest.mock import AsyncMock

import bcrypt
import jwt
import pytest

from base_api.core.exceptions import AuthenticationError
from base_api.modules.auth.schemas import LoginUserSchema, RegisterUserSchema
from base_api.modules.auth.service import AuthService
from base_api.modules.user.models import User
from base_api.modules.user.repository import UserRepository


@pytest.fixture()
def user_repo() -> UserRepository:
    return AsyncMock(spec=UserRepository)


@pytest.fixture()
def auth_service(user_repo, mock_settings) -> AuthService:
    return AuthService(user_repo=user_repo, settings=mock_settings)


async def test_register_user(auth_service, user_repo):
    data = RegisterUserSchema(login='test', password='Test!2#45')
    user_repo.create.side_effect = lambda user: user

    result = await auth_service.register(data)

    assert isinstance(result, User)
    assert result.password != data.password


async def test_login(auth_service, user_repo):
    data = LoginUserSchema(login='test', password='test')
    sub = 123
    hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())

    def return_user(login):
        user = User(user_id=sub, login=login, password=hashed_password.decode('utf-8'))
        return user

    user_repo.get_by_login.side_effect = return_user

    result = await auth_service.login(data)

    decoded = jwt.decode(
        result,
        auth_service.settings.API_KEY,
        algorithms=[auth_service.settings.JWT_ALGORITHM],
    )
    assert isinstance(result, str)
    assert decoded['sub'] == str(sub)
    assert decoded['iat']
    assert decoded['exp']


async def test_login_user_not_found(auth_service, user_repo):
    data = LoginUserSchema(login='test', password='test')
    user_repo.get_by_login.side_effect = lambda login: None

    with pytest.raises(AuthenticationError):
        result = await auth_service.login(data)


async def test_login_invalid_password(auth_service, user_repo):
    data = LoginUserSchema(login='test', password='test')
    hashed_wrong_password = bcrypt.hashpw(b'WRONG_PASSOWRD', bcrypt.gensalt())

    def return_user(login):
        user = User(
            user_id='123', login=login, password=hashed_wrong_password.decode('utf-8')
        )
        return user

    user_repo.get_by_login.side_effect = return_user

    with pytest.raises(AuthenticationError):
        result = await auth_service.login(data)
