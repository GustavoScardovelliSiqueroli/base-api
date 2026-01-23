import string

import pytest
from pydantic import ValidationError

from base_api.modules.auth.schemas import RegisterUserSchema

VALID_LOGIN: str = "test"
VALID_PASSWORD: str = "Test123@!"


def test_user_password_need_8_characters():
    with pytest.raises(ValidationError):
        RegisterUserSchema(login=VALID_LOGIN, password="1234567")


def test_user_password_need_number():
    with pytest.raises(ValidationError):
        RegisterUserSchema(login=VALID_LOGIN, password="abcdefgh")


def test_user_password_need_upper_char():
    with pytest.raises(ValidationError):
        RegisterUserSchema(login=VALID_LOGIN, password=VALID_PASSWORD.lower())


def test_user_password_need_special():
    special_chars = set(string.punctuation)
    without_special = "".join("a" if c in special_chars else c for c in VALID_PASSWORD)

    with pytest.raises(ValidationError):
        RegisterUserSchema(login=VALID_LOGIN, password=without_special)


def test_user_password_need_lower():
    with pytest.raises(ValidationError):
        RegisterUserSchema(login=VALID_LOGIN, password=VALID_PASSWORD.upper())


def test_user_password_valid():
    RegisterUserSchema(login=VALID_LOGIN, password=VALID_PASSWORD)
