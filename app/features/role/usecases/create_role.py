from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from ..repository import GetRole
from app.utilities.exceptions import DatabaseError, NotFoundException


async def create_role(role_id : UUID, db : AsyncSession):
    role = await GetRole.get_role_by_id(role_id, db)
    if not role:
        raise NotFoundException("Role")
    return role