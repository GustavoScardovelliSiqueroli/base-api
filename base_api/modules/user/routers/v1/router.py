from fastapi import APIRouter, Depends

from base_api.modules.user.dependencies import get_user_service
from base_api.modules.user.schemas import PublicUserSchema
from base_api.modules.user.service import UserService
from base_api.shared.response_schemas import ApiResponse

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=ApiResponse[list[PublicUserSchema]])
def get_users(
    user_service: UserService = Depends(get_user_service),
) -> ApiResponse[list[PublicUserSchema]]:
    users = user_service.get_all_users()
    return ApiResponse(data=[PublicUserSchema.model_validate(user) for user in users])
