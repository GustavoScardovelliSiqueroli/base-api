from unittest.mock import AsyncMock
from uuid import UUID

from httpx import ASGITransport, AsyncClient

from base_api.core.exceptions import AuthenticationError
from base_api.main import app
from base_api.modules.auth.dependencies import get_auth_service
from base_api.modules.auth.service import AuthService
from base_api.modules.user.models import User

AUTH_PREFIX = '/api/v1/auth'


async def test_register_success():
    fake_user = User(
        user_id=UUID('40bb1a39-2d93-466b-a291-855e4cb53daa'),
        login='test',
        password='fakehashedpassword',
    )
    auth_service_mock = AsyncMock(spec=AuthService)
    auth_service_mock.register.return_value = fake_user
    app.dependency_overrides[get_auth_service] = lambda: auth_service_mock
    payload = {'login': 'test', 'password': '123@Abcd'}

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        response = await client.post(f'{AUTH_PREFIX}/register', json=payload)

    body = response.json()
    assert response.status_code == 201
    assert body['success'] is True
    assert body['data']['login'] == 'test'
    assert 'password' not in body['data']
    app.dependency_overrides.clear()


async def test_login_success():
    auth_service_mock = AsyncMock(spec=AuthService)
    auth_service_mock.login.return_value = 'faketoken'
    app.dependency_overrides[get_auth_service] = lambda: auth_service_mock

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        response = await client.post(
            f'{AUTH_PREFIX}/login', data={'username': 'test', 'password': 'test'}
        )

    assert response.status_code == 200
    body = response.json()
    assert body == {'access_token': 'faketoken', 'token_type': 'bearer'}
    app.dependency_overrides.clear()


async def test_login_auth_error():
    auth_service_mock = AsyncMock(spec=AuthService)
    auth_service_mock.login.side_effect = AuthenticationError()
    app.dependency_overrides[get_auth_service] = lambda: auth_service_mock

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        response = await client.post(
            f'{AUTH_PREFIX}/login', data={'username': 'test', 'password': 'test'}
        )

    assert response.status_code == 401
    body = response.json()
    assert body == {'detail': 'Invalid credentials'}
    assert not hasattr(body, 'success')
