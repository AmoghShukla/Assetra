from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_organization import UserOrganization
from app.utilities.exceptions import DatabaseError


class UserOrganizationRepository:

    @staticmethod
    async def create_user_organization(payload, db : AsyncSession):
        try:
            db.add(payload)
            await db.commit()
            await db.refresh(payload)
            return payload
        except SQLAlchemyError as e:
            raise DatabaseError()

    @staticmethod
    async def get_user_organization_by_user_id(user_id, db : AsyncSession):
        try:
            statement = (
                select(UserOrganization)
                .where(
                    UserOrganization.user_id == user_id, 
                    UserOrganization.is_deleted == False
                    )
            )
            user_organization_obj = await db.execute(statement)
            user_organization = user_organization_obj.scalar_one_or_none()
            return user_organization
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def already_allocated_user_organization(user_id, organization_id, db : AsyncSession):
        try:
            statement = (
                select(UserOrganization)
                .where(
                    UserOrganization.user_id == user_id, 
                    UserOrganization.organization_id == organization_id,
                    UserOrganization.is_deleted == False
                    )
            )
            user_organization_obj = await db.execute(statement)
            user_organization = user_organization_obj.scalars().first()
            return user_organization
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_all_user_organization_allocations(db : AsyncSession):
        try:
            statement = (
                select(UserOrganization)
                .where(
                    UserOrganization.is_deleted==False
                )
            )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_user_by_organization(organization_id : UUID, db : AsyncSession):
        try:
            statement = (
                select(UserOrganization)
                .where(
                    UserOrganization.organization_id==organization_id,
                    UserOrganization.is_deleted==False
                )
            )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()