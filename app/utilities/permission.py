'''function to require permission to access a specific route or something similar'''

from functools import wraps
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.permissions.repository import PermissionRepository


async def resolve_user_permissions(user_id: UUID, db: AsyncSession):
    '''
    final permissions for a user will essentially be:
    (role_permissions + granted_permissions) - revoked_permissions
    '''

    '''Fetching the Roles Based Permission'''
    role_permission = await PermissionRepository.fetch_roles_based_permission(user_id, db)

    '''Fetching the User Based Permission'''
    user_level_permission = await PermissionRepository.fetch_user_permissions(user_id, db)

    granted_permission = {perm.permission.permission_name for perm in user_level_permission if perm.is_granted and not perm.is_revoked}
    revoked_permission = {perm.permission.permission_name for perm in user_level_permission if perm.is_revoked}

    final_permission = (role_permission | granted_permission) - revoked_permission
    return sorted(final_permission)

async def check_permission(user_id: UUID, permission_name: str, db: AsyncSession) -> bool:
    perms = await resolve_user_permissions(user_id, db)
    return permission_name in perms