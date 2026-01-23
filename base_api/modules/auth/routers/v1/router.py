from fastapi import APIRouter, Depends

from base_api.modules.auth.dependencies import get_auth_service
from base_api.modules.auth.schemas import RegisterUserSchema
from base_api.modules.auth.service import AuthService
from base_api.modules.user.schemas import PublicUserSchema
from base_api.shared.response_schemas import ApiResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse[PublicUserSchema])
def register(
    data: RegisterUserSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> ApiResponse[PublicUserSchema]:
    user = auth_service.register(data)
    return ApiResponse(data=PublicUserSchema.model_validate(user))
