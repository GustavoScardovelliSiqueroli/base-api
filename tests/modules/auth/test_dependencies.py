from datetime import datetime, timedelta
from unittest.mock import AsyncMock
from uuid import UUID

import jwt
import pytest

from base_api.core.exceptions import AuthenticationError
from base_api.modules.auth.dependencies import get_auth_service, get_current_user
from base_api.modules.auth.service import AuthService
from base_api.modules.user.models import User
from base_api.modules.user.repository import UserRepository


async def test_get_current_user_success(mock_settings):
    now = datetime.now()
    payload = {
        'sub': '40bb1a39-2d93-466b-a291-855e4cb53daa',
        'iat': int(now.timestamp()),
        'exp': int((now + timedelta(hours=999999)).timestamp()),
    }
    fake_token = jwt.encode(
        payload, mock_settings.API_KEY, algorithm=mock_settings.JWT_ALGORITHM
    )
    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_user_repo.get_by_id.return_value = User(
        user_id=UUID('40bb1a39-2d93-466b-a291-855e4cb53daa'),
        login='test',
        password='test',
    )
    result = await get_current_user(fake_token, mock_user_repo, mock_settings)
    assert isinstance(result, User)


async def test_get_current_user_fail_jwt(mock_settings):
    wrong_token = 'wrongtoken'
    mock_user_repo = AsyncMock(spec=UserRepository)

    with pytest.raises(AuthenticationError):
        result = await get_current_user(wrong_token, mock_user_repo, mock_settings)


async def test_get_current_user_fail_withour_sub(mock_settings):
    now = datetime.now()
    payload = {
        'iat': int(now.timestamp()),
        'exp': int((now + timedelta(hours=999999)).timestamp()),
    }
    fake_token = jwt.encode(
        payload, mock_settings.API_KEY, algorithm=mock_settings.JWT_ALGORITHM
    )
    mock_user_repo = AsyncMock(spec=UserRepository)

    with pytest.raises(AuthenticationError):
        result = await get_current_user(fake_token, mock_user_repo, mock_settings)


async def test_get_current_user_fail_user_not_found(mock_settings):
    now = datetime.now()
    payload = {
        'sub': '40bb1a39-2d93-466b-a291-855e4cb53daa',
        'iat': int(now.timestamp()),
        'exp': int((now + timedelta(hours=999999)).timestamp()),
    }
    fake_token = jwt.encode(
        payload, mock_settings.API_KEY, algorithm=mock_settings.JWT_ALGORITHM
    )
    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_user_repo.get_by_id.return_value = None

    with pytest.raises(AuthenticationError):
        result = await get_current_user(fake_token, mock_user_repo, mock_settings)


def test_get_auth_service(mock_settings):
    mock_user_repo = AsyncMock()

    result = get_auth_service(mock_user_repo, mock_settings)

    assert isinstance(result, AuthService)
