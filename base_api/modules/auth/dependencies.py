from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from base_api.core.configs import Settings, get_settings
from base_api.core.exceptions import AuthenticationError
from base_api.modules.auth.service import AuthService
from base_api.modules.user.dependencies import get_user_repository
from base_api.modules.user.models import User
from base_api.modules.user.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
) -> User:
    try:
        payload = jwt.decode(
            token, settings.API_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        raise AuthenticationError('Invalid token') from e

    user_id: str = payload.get('sub')
    if not user_id:
        raise AuthenticationError('Invalid token')

    user = await user_repo.get_by_id(UUID(user_id))
    if not user:
        raise AuthenticationError('User not found')

    return user


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    return AuthService(user_repo=user_repo, settings=settings)
