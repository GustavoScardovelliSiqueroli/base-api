import pytest

from base_api.core.configs import Settings


@pytest.fixture
def mock_settings() -> Settings:
    return Settings(ACCESS_TOKEN_EXPIRE_HOURS=24, API_KEY='DEV')
