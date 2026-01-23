import string

from pydantic import BaseModel
from pydantic.functional_validators import field_validator


class RegisterUserSchema(BaseModel):
    login: str
    password: str

    @field_validator("password")
    @classmethod
    def check_password(cls, password: str) -> str:
        has_decimal: bool = False
        has_especial: bool = False
        has_upper: bool = False
        has_lower: bool = False

        special_chars = set(string.punctuation)

        if len(password) < 8:
            raise ValueError("Senha precisa ter ao menos 8 caracteres")
        for c in password:
            if c.isdecimal():
                has_decimal = True
            elif c in special_chars:
                has_especial = True
            elif c == c.upper():
                has_upper = True
            elif c == c.lower():
                has_lower = True

        if not has_decimal:
            raise ValueError("Senha precisa ter ao menos um numero")
        if not has_upper:
            raise ValueError("Senha precisa ter ao menos uma letra maiúscula")
        if not has_especial:
            raise ValueError("Senha precisa ter ao menos um caracter especial")
        if not has_lower:
            raise ValueError("Senha precisa ter ao menos um caracter minúsculo")

        return password
