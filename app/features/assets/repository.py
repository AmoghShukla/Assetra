from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.asset_assignment import AssetAssignment
from app.models.asset_type import AssetType
from app.models.user import User
from app.models.user_organization import UserOrganization
from app.utilities.enums import RoleName
from app.utilities.exceptions import DatabaseError

class AssetRepository:

    @staticmethod
    async def create_asset_type(data, db: AsyncSession):
        try:
            db.add(data)
            await db.commit()
            await db.refresh(data)
            return data
        except SQLAlchemyError:
            raise DatabaseError()
        
    @staticmethod
    async def get_all_asset_types(db):
        try:
            statement = (
                select(AssetType)
                .where(
                    AssetType.is_deleted == False)
            )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError:
            raise DatabaseError()
    
    @staticmethod
    async def get_all_asset_types_by_organization_id(organization_id, db):
        try:
            statement = (
                select(AssetType)
                .where(
                    AssetType.organization_id == organization_id,
                    AssetType.is_deleted == False
                    )
            )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError:
            raise DatabaseError()
    
    @staticmethod
    async def get_asset_types_by_type_and_organization_id(asset_type_id, organization_id, db):
        try:
            statement = (
                select(AssetType)
                .where(
                    AssetType.asset_type_id == asset_type_id,
                    AssetType.organization_id == organization_id,
                    AssetType.is_deleted == False,
                )
            )
            result = await db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            raise DatabaseError()
    

    @staticmethod
    async def get_asset_types_by_name(asset_name, organization_id, db):
        try:
            statement = (
                select(AssetType)
                .where(
                    AssetType.asset_name == asset_name,
                    AssetType.organization_id == organization_id,
                    AssetType.is_deleted == False,
                )
            )
            result = await db.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError:
            raise DatabaseError()
        
    
    @staticmethod
    async def get_employee_by_organization_id(employee_id : UUID, organization_id : UUID, db : AsyncSession):
        try:
            statement = (
                select(UserOrganization.organization_id)
                .where(
                    UserOrganization.user_id == employee_id,
                    UserOrganization.organization_id == organization_id,
                    UserOrganization.is_deleted == False,
                )
            )
            result = await db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseError() 

    @staticmethod
    async def get_org_asset(asset_id: UUID, org_id: UUID, db: AsyncSession):
        try:
            statement = (
                select(Asset)
                .where(
                    Asset.asset_id == asset_id, 
                    Asset.organization_id == org_id, 
                    Asset.is_deleted == False
                    )
                )
            result = await db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            raise DatabaseError()
        
    @staticmethod
    async def get_asset_metrics(current_user: User, db: AsyncSession):
        try:
            statement = (
            select(
                Asset.asset_status, 
                func.count(Asset.asset_id)
            )
            .where(
                Asset.organization_id == current_user._organization_id, 
                Asset.is_deleted == False
            )
            .group_by(Asset.asset_status)
            )
            result = await db.execute(statement)
            return result.all()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_asset_by_code(asset_code, db):
        try:
            statement = (
                select(Asset)
                .where(
                    Asset.asset_code == asset_code, 
                    Asset.is_deleted == False
                    )
                )
            result = await db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_alloted_assests(current_user, db):
        try:
            if current_user._role == RoleName.EMPLOYEE.value:
                ''' Employee sees only their assigned assets'''
                statement = (
                    select(Asset)
                    .join(AssetAssignment, AssetAssignment.asset_id == Asset.asset_id)
                    .where(
                        AssetAssignment.assigned_to == current_user.user_id,
                        AssetAssignment.is_deleted == False,
                        Asset.is_deleted == False,
                    )
                )
            else:
                statement = select(Asset).where(Asset.organization_id == current_user._organization_id, Asset.is_deleted == False)

            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def update_asset(data, asset, current_user, db):
        try:
            if data.asset_name:
                asset.asset_name = data.asset_name
            if data.asset_description is not None:
                asset.asset_description = data.asset_description
            asset.updated_by = current_user.user_id
            db.add(asset)
            await db.flush()
            await db.refresh(asset)
            return asset
        except SQLAlchemyError as e:
            raise DatabaseError()
        
    @staticmethod
    async def change_asset_status(asset, new_status, user_id, db):
        try:
            asset.asset_status = new_status
            asset.updated_by = user_id
            db.add(asset)
            await db.flush()
            await db.refresh(asset)
            return asset
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def delete_asset(asset, db : AsyncSession):
        try:
            asset.is_deleted = True
            db.add(asset)
            return {"message": "Asset deleted"}
        except SQLAlchemyError as e:
            raise DatabaseError()
        

# --------------- Assest Assignment ---------------------

class AssetAssignmentRepository:

    @staticmethod
    async def create_asset_assignment(data, db: AsyncSession):
        try:
            db.add(data)
            await db.commit()
            await db.refresh(data)
            return data
        except SQLAlchemyError:
            raise DatabaseError()
    
    @staticmethod
    async def get_asset_assignment_with_asset_id(asset_id, db : AsyncSession):
        try:
            statement = (
                select(AssetAssignment).where(
                    AssetAssignment.asset_id == asset_id,
                    AssetAssignment.is_deleted == False,
                )
            )
            result = await db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def soft_delete_asset_assignment(asset_assignment, db):
        try:
            asset_assignment.is_deleted = True
            db.add(asset_assignment)
            return {"message": "Asset Assignment deleted"}
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def change_asset_assignment_status(asset_assignment, new_status, user_id, db):
        try:
            asset_assignment.asset_status = new_status
            asset_assignment.updated_by = user_id
            db.add(asset_assignment)
            await db.flush()
            await db.refresh(asset_assignment)
            return asset_assignment
        except SQLAlchemyError as e:
            raise DatabaseError()
    