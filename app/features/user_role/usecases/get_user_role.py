from app.features.user_role.schemas import UserRoleResponse
from app.features.users.controllers import get_user_by_id
from app.utilities.exceptions import NotFoundException
from app.features.user_role.repository import UserRoleAllocation


async def get_user_role_by_user_id(user_id, db):
    user = get_user_by_id(user_id, db)
    if not user:
        raise NotFoundException('User')
    role = await UserRoleAllocation.get_user_role_by_user_id(user_id, db)
    return UserRoleResponse(
        user_id=user_id,
        role_id=role.role_id,
        role_name=role.role_name
    )