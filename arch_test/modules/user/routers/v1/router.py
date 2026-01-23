from fastapi import APIRouter, Depends

from arch_test.modules.user.dependencies import get_user_service
from arch_test.modules.user.schemas import CreateUserSchema, PublicUserSchema
from arch_test.modules.user.service import UserService
from arch_test.shared.response_schemas import ApiResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=ApiResponse[PublicUserSchema])
def create_user(
    data: CreateUserSchema,
    user_service: UserService = Depends(get_user_service),
) -> ApiResponse[PublicUserSchema]:
    user = user_service.create_user(data)
    return ApiResponse(data=PublicUserSchema.model_validate(user))


@router.get("/", response_model=ApiResponse[list[PublicUserSchema]])
def get_users(
    user_service: UserService = Depends(get_user_service),
) -> ApiResponse[list[PublicUserSchema]]:
    users = user_service.get_all_users()
    return ApiResponse(data=[PublicUserSchema.model_validate(user) for user in users])
