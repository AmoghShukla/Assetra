from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.role import Role
from app.models.user import User
from app.utilities.enums import RoleName
from app.utilities.exceptions import DatabaseError


class GetRole:

    @staticmethod
    async def get_user_and_role_by_user_id(user_id, db: AsyncSession):
        statement = (
            select(User)
            .where(User.user_id == user_id, User.is_deleted == False)
            .options(selectinload(User.user_roles))
        )
        result = await db.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def get_role_by_id(role_id, db: AsyncSession):
        try:
            result = await db.execute(
                select(Role).where(
                    Role.role_id == role_id,
                    Role.is_deleted == False
                )
            )
            role = result.scalar_one_or_none()
            return role
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_role_by_name(current_role, db: AsyncSession):
        try:
            result = await db.execute(
                select(Role).where(
                    Role.role_name == current_role,
                    Role.is_deleted == False
                )
            )
            role = result.scalar_one_or_none()
            return role
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_all_roles(db : AsyncSession):
        try:
            statement = (
                select(Role)
                .where(Role.is_deleted==False)
            )
            roles =  await db.execute(statement)
            return roles.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()