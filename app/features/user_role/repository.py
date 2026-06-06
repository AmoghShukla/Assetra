

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.role import Role
from app.models.user_roles import UserRole
from app.utilities.exceptions import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession


class UserRoleAllocation:

    @staticmethod
    async def create_user_role(payload, db: AsyncSession):
        try:
            user_role = UserRole(
                user_id=payload.user_id,
                role_id=payload.role_id
            )
            db.add(user_role)
            await db.flush()
            await db.refresh(user_role)
            return user_role
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_user_role_by_user_id(user_id, db):
        try:
            statement = (
                select(Role)
                .join(UserRole, UserRole.role_id == Role.role_id)
                .where(UserRole.user_id == user_id, UserRole.is_deleted == False)
            )
            role_name_obj = await db.execute(statement)
            return role_name_obj.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseError()