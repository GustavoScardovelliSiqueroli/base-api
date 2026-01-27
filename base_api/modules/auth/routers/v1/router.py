from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from base_api.core.exceptions import AuthenticationError
from base_api.modules.auth.dependencies import get_auth_service
from base_api.modules.auth.schemas import (
    LoginResponseSchema,
    LoginUserSchema,
    RegisterUserSchema,
)
from base_api.modules.auth.service import AuthService
from base_api.modules.user.schemas import PublicUserSchema
from base_api.shared.response_schemas import ApiResponse

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[PublicUserSchema],
)
async def register(
    data: RegisterUserSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> ApiResponse[PublicUserSchema]:
    user = await auth_service.register(data)
    return ApiResponse(data=PublicUserSchema.model_validate(user))


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=LoginResponseSchema,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponseSchema:
    data = LoginUserSchema(login=form_data.username, password=form_data.password)
    try:
        token = await auth_service.login(data)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from e
    return LoginResponseSchema(access_token=token)
