from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import organization
from app.models.user import User
from app.models.user_organization import UserOrganization
from app.utilities.exceptions import DatabaseError

class UserRepository:
    
    @staticmethod
    async def get_user_by_id(user_id, db: AsyncSession):
        statement = (
            select(User)
            .where(User.user_id == user_id, User.is_deleted == False)
            .options(selectinload(User.user_roles)) 
        )
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    
    @staticmethod
    async def get_user_by_email(email_id: str, db: AsyncSession) -> User | None:
        try:
            result = await db.execute(
                select(User).where(
                    User.user_email == email_id,
                    User.is_deleted == False
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise DatabaseError('Error fetching user by email') from e

    @staticmethod
    async def get_all_users(organization_id, db):
        try:
            stmt = (
                select(User)
                .join(UserOrganization, UserOrganization.user_id == User.user_id)
                .where(UserOrganization.organization_id == organization_id, UserOrganization.is_deleted == False, User.is_deleted == False)
            )
            result = await db.execute(stmt)
            users = result.scalars().all()
            return users
        except SQLAlchemyError as e:
            raise DatabaseError('Error fetching all the users by organization') from e
    
    @staticmethod
    async def manage_it_access(payload, db):
        try:
            db.add(payload)
            await db.commit()
            return payload
        except SQLAlchemyError as e:
            raise DatabaseError()
        
    @staticmethod
    async def update_user(user, data, db):
        try:
            if data.user_name:
                user.user_name = data.user_name
            db.add(user)
            await db.flush()
            await db.refresh(user)
            return user
        except SQLAlchemyError as e:
            raise DatabaseError('Error while updating the user') from e
        
    @staticmethod
    async def delete_user(user, data, db):
        try:
            user.is_deleted = True
            db.add(user)
            return {"message": "User deleted successfully"}
            await db.commit()
        except SQLAlchemyError as e:
            raise DatabaseError('Error while updating the user') from e
        
    