from ..schemas import CreateUserRole
from app.features.users.repository import UserRepository 
from app.utilities.exceptions import NotFoundException
from app.features.role.repository import GetRole
from app.features.user_role.repository import UserRoleAllocation

from sqlalchemy.ext.asyncio import AsyncSession

async def create_intermediate_user_role(
    payload : CreateUserRole,
    db : AsyncSession    
):
    user = await UserRepository.get_user_by_id(payload.user_id, db)
    if not user:
        raise NotFoundException("User")
    
    role = await GetRole.get_role_by_id(payload.role_id, db)
    if not role:
        raise NotFoundException("Role")
    
    allotment = await UserRoleAllocation.create_user_role(payload, db)
    return allotment
    
    