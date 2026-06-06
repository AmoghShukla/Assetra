from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.features.user_organization.repository import UserOrganizationRepository
from app.features.user_role.repository import UserRoleAllocation
from app.features.users.usecases.get_user import get_user_by_id
from app.models.user import User
from app.models.user_organization import UserOrganization
from app.utilities.exceptions import NotFoundException, ForbiddenException
from app.utilities.enums import RoleName
from app.utilities.permission import resolve_user_permissions
from app.features.users.schemas import UserPermissionsResponse


async def get_user_permissions(
    target_user_id: UUID,
    requesting_user: User,
    db: AsyncSession,
) -> UserPermissionsResponse:
    
    '''Only SUPERADMIN and ORG_ADMIN can view permissions'''
    if requesting_user._role not in [RoleName.SUPERADMIN.value, RoleName.ORG_ADMIN.value]:
        raise ForbiddenException("Only Superadmin and Org Admin can view user permissions")

    '''Org admin can only view users in their own organization'''
    if requesting_user._role == RoleName.ORG_ADMIN.value:
        target_organization = await UserOrganizationRepository.get_user_organization_by_user_id(target_user_id, db)
        target_organization_id = target_organization.organization_id
        if target_organization_id != requesting_user._organization_id:
            raise ForbiddenException("You can only view permissions of users in your organization")

    user = await get_user_by_id(target_user_id, db)
    if not user:
        raise NotFoundException("User")

    fetched_role = await UserRoleAllocation.get_user_role_by_user_id(target_user_id, db)
    role = fetched_role.role_name
    permissions = await resolve_user_permissions(target_user_id, db)

    return UserPermissionsResponse(user_id=target_user_id, role=role, permissions=permissions)
