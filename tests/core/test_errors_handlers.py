from fastapi import Request
from fastapi.responses import JSONResponse

from base_api.core.errors_handlers import domain_error_handler
from base_api.core.exceptions import DomainException, ErrorCode


def test_domain_error_handler():
    domain_exec = DomainException('test', ErrorCode.AUTH_FAIL, 401)
    request = Request(scope={'type': 'http'})

    result = domain_error_handler(request, domain_exec)

    assert isinstance(result, JSONResponse)
    assert result.status_code == 401
    assert (
        result.body
        == b'{"success":false,"error":{"code":"AUTH_FAIL","message":"test"}}'
    )
