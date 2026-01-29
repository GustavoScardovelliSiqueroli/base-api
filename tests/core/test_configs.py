from pytest import MonkeyPatch

from base_api.core.configs import Settings, get_settings


def test_get_settings():
    get_settings.cache_clear()
    mk = MonkeyPatch()
    mk.setenv('API_KEY', 'test_get_settings-key')
    mk.setenv('ACCESS_TOKEN_EXPIRE_HOURS', '12345')

    settings = get_settings()

    assert isinstance(settings, Settings)
    assert settings.API_KEY == 'test_get_settings-key'
    assert settings.ACCESS_TOKEN_EXPIRE_HOURS == 12345
