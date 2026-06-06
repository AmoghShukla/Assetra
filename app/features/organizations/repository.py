
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.organization import Organization
from app.utilities.exceptions import DatabaseError


class OrganizationRepository:

    @staticmethod
    async def create_organization(payload, db):
        try:
            db.add(payload)
            await db.flush()
            await db.refresh(payload)
            return payload
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_organization_by_id(organization_id : UUID, db : AsyncSession):
        try:
            statement = (
                select(Organization)
                .where(
                    Organization.organization_id == organization_id, 
                    Organization.is_deleted == False
                    )
                )
            result = await db.execute(statement) 
            return result.scalars().first() 
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_organization_by_name(organization_name, db : AsyncSession):
        try:
            statement = (
                select(Organization)
                .where(
                    Organization.organization_name == organization_name, 
                    Organization.is_deleted == False
                    )
                )
            result = db.execute(statement)
            org = result.scalar_one_or_none()
            return org
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_all_organization(db : AsyncSession):
        try:
            statement = (
                select(Organization)
                .where(
                    Organization.is_deleted == False
                    )
                )
            result = await db.execute(statement)
            org = result.scalars().all()
            return org
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def delete_organization(org, db):
        db.add(org)
        return {"message": "Organization deleted successfully"}