from fastapi import APIRouter, Depends

from arch_test.modules.auth.dependencies import get_auth_service
from arch_test.modules.auth.schemas import RegisterUserSchema
from arch_test.modules.auth.service import AuthService
from arch_test.modules.user.schemas import PublicUserSchema
from arch_test.shared.response_schemas import ApiResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse[PublicUserSchema])
def register(
    data: RegisterUserSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> ApiResponse[PublicUserSchema]:
    user = auth_service.register(data)
    return ApiResponse(data=PublicUserSchema.model_validate(user))
