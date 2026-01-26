from enum import Enum


class ErrorCode(str, Enum):
    REC_DUPLICADO = 'REC_DUPLICADO'
    AUTH_FAIL = 'AUTH_FAIL'


class DomainException(Exception):
    def __init__(
        self, message: str, internal_code: ErrorCode, http_status_code: int
    ) -> None:
        self.internal_code = internal_code
        self.message = message
        self.http_status_code = http_status_code


class DuplicatedError(DomainException):
    def __init__(self, column: str) -> None:
        message = f'Já existe esse valor no campo {column}'
        super().__init__(message, ErrorCode.REC_DUPLICADO, 400)


class AuthenticationError(DomainException):
    def __init__(self, message: str = 'Autenticação falhou') -> None:
        super().__init__(message, ErrorCode.AUTH_FAIL, 401)
