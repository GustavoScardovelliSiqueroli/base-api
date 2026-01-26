import string

from pydantic import BaseModel
from pydantic.functional_validators import field_validator


class LoginUserSchema(BaseModel):
    login: str
    password: str


class RegisterUserSchema(BaseModel):
    login: str
    password: str

    @field_validator('password')
    @classmethod
    def check_password(cls, password: str) -> str:
        has_decimal: bool = False
        has_special: bool = False
        has_upper: bool = False
        has_lower: bool = False

        special_chars = set(string.punctuation)

        if len(password) < 8:
            raise ValueError('Senha precisa ter ao menos 8 caracteres')
        for c in password:
            if c.isdecimal():
                has_decimal = True
            elif c in special_chars:
                has_special = True
            elif c == c.upper():
                has_upper = True
            elif c == c.lower():
                has_lower = True

        RegisterUserSchema._handle_password_error(
            has_decimal, has_special, has_upper, has_lower
        )

        return password

    @classmethod
    def _handle_password_error(
        cls, has_decimal: bool, has_special: bool, has_upper: bool, has_lower: bool
    ) -> None:
        if not has_decimal:
            raise ValueError('Senha precisa ter ao menos um numero')
        if not has_upper:
            raise ValueError('Senha precisa ter ao menos uma letra maiúscula')
        if not has_special:
            raise ValueError('Senha precisa ter ao menos um caracter especial')
        if not has_lower:
            raise ValueError('Senha precisa ter ao menos um caracter minúsculo')
