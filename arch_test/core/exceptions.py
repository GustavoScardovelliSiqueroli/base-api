from enum import Enum


class ErrorCode(str, Enum):
    REC_DUPLICADO = "REC_DUPLICADO"


class DomainException(Exception):
    def __init__(
        self, message: str, internal_code: ErrorCode, http_status_code: int
    ) -> None:
        self.internal_code = internal_code
        self.message = message
        self.http_status_code = http_status_code


class DuplicatedError(DomainException):
    def __init__(self, column: str) -> None:
        message = f"Já existe esse valor no campo {column}"
        super().__init__(message, ErrorCode.REC_DUPLICADO, 400)
