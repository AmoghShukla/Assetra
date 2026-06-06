
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.permissions.repository import PermissionRepository
from app.features.user_role.repository import UserRoleAllocation
from app.features.users.schemas import UpdateUserRequest, UserResponse
from app.features.users.repository import UserRepository
from app.models.user import User
from app.models.user_permission import UserPermission
from app.utilities.enums import RoleName
from app.utilities.exceptions import BadRequestException, NotFoundException


async def update_user(user_id: UUID, data: UpdateUserRequest, current_user: User, db: AsyncSession) -> UserResponse:
    """Updating the User"""
    user = await UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise NotFoundException("User")
    updated_user = await UserRepository.update_user(user, data, db)
    return UserResponse.model_validate(updated_user)

async def delete_user(user_id: UUID, current_user: User, db: AsyncSession) -> dict:
    """Deleting the User"""
    user = await UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise NotFoundException("User")


async def revoke_it_admin_asset_permission(target_user_id: UUID, reason: str, revoker: User, db: AsyncSession) -> dict:
    """Superadmin revokes IT Admin's ability to manage assets."""
    
    '''Verifying that the target is an IT_ADMIN'''
    role_result = await UserRoleAllocation.get_user_role_by_user_id(target_user_id, db)
    role = role_result.role_name
    if role != RoleName.IT_ADMIN.value:
        raise BadRequestException("Can only revoke permissions from IT Admins")

    '''Find all the asset-related permissions of the IT ADMIN and revoking them'''
    permissions = await PermissionRepository.get_permission_by_topic('asset', db)

    now = datetime.now(timezone.utc)
    for permission in permissions:
        user_permission_exists = await PermissionRepository.get_user_permission_by_user_and_permission_id(
            target_user_id, 
            permission.permission_id, 
            db
            )
        if user_permission_exists:
            user_permission_exists.is_revoked = True
            user_permission_exists.revoked_by = revoker.user_id
            user_permission_exists.revoked_at = now
            user_permission_exists.revoking_reason = reason
            update = await UserRepository.revoke_it_access(user_permission_exists)
                        
        else:
            user_permission_exist = UserPermission(
                user_id=target_user_id,
                permission_id=permission.permission_id,
                is_granted=False,
                is_revoked=True,
                revoked_by=revoker.user_id,
                revoked_at=now,
                revoking_reason=reason,
                )
            update = await UserRepository.manage_it_access(user_permission_exist)

    return {"message": "Asset permissions revoked from IT Admin"}



async def restore_it_admin_asset_permission(target_user_id: UUID, restorer: User, db: AsyncSession) -> dict:
    """Superadmin restores IT Admin's ability to manage assets."""
    asset_permissions = await PermissionRepository.get_permission_by_user_id_and_status(target_user_id, db)
    for ap in asset_permissions:
        ap.is_revoked = False
        ap.revoking_reason = None
        await UserRepository.manage_it_access(ap, db)

    return {"message": "Asset permissions restored for IT Admin"}
