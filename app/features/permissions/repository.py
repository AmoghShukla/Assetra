from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user_permission import UserPermission
from app.models.user_roles import UserRole
from app.utilities.exceptions import DatabaseError


class PermissionRepository:

    @staticmethod
    async def get_permission_by_name(permission_name, db):
        try:
            statement = (
                select(Permission)
                .where(
                    Permission.permission_name == permission_name,
                    Permission.is_deleted==False
                    )
                )
            result = await db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def fetch_roles_based_permission(user_id, db):
        try:
            statement = (
                select(Permission.permission_name)
                .join(
                    RolePermission, 
                    RolePermission.permission_id == Permission.permission_id
                )
                .join(
                    UserRole,
                    UserRole.role_id == RolePermission.role_id
                )
                .where(
                    UserRole.user_id == user_id, 
                    UserRole.is_deleted == False
                    )
                )
            result = await db.execute(statement)
            return set(result.scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def fetch_user_permissions(user_id, db):
        try:
            statement = (
                select(UserPermission)
                .where(
                    UserPermission.user_id == user_id, 
                    UserPermission.is_deleted == False
                )
            )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_permission_by_topic(type, db):
        try:
            statement = (
                select(Permission)
                .where(Permission.permission_name.like(f"{type}:%"))
            )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()
        
    @staticmethod
    async def get_user_permission_by_user_and_permission_id(user_id, permission_id, db):
        try:    
            statement = (
                select(UserPermission).where(
                    UserPermission.user_id == user_id,
                    UserPermission.permission_id == permission_id,
                    UserPermission.is_deleted == False,
                )
            )
            result = await db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_permission_by_user_id_and_status(user_id, db):
        try:
            statement = (
                select(UserPermission)
                .join(Permission, Permission.permission_id == UserPermission.permission_id)
                .where(
                    UserPermission.user_id == user_id,
                    UserPermission.is_revoked == True,
                    UserPermission.is_deleted == False,
                    Permission.permission_name.like("asset:%"),
                )
            )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()