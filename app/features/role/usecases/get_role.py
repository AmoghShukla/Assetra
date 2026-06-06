from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from ..repository import GetRole
from app.utilities.exceptions import DatabaseError, NotFoundException


async def get_role_by_id(role_id : UUID, db : AsyncSession):
    role = await GetRole.get_role_by_id(role_id, db)
    if not role:
        raise NotFoundException("Role")
    return role

async def get_role_by_name(role_name , db : AsyncSession):
    role = await GetRole.get_role_by_name(role_name, db)
    if not role:
        raise NotFoundException("Role")
    return role

async def get_all_roles(db : AsyncSession):
    return await GetRole.get_all_roles(db)