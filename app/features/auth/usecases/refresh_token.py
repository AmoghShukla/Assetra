from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.features.user_organization.repository import UserOrganizationRepository
from app.features.user_role.repository import UserRoleAllocation
from app.features.users.repository import UserRepository
from app.models import User, UserRole, UserOrganization, Role
from app.utilities.security import Security
from app.utilities.exceptions import UnauthorizedException
from app.features.auth.schemas import RefreshTokenRequest, TokenResponse


async def refresh_token(data: RefreshTokenRequest, db: AsyncSession) -> TokenResponse:
    payload = Security.decode_token(data.refresh_token)
    if payload.get("type") != "refresh":
        raise UnauthorizedException("Invalid token type")

    user_id = (payload["sub"])
    user = await UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise UnauthorizedException("User not found")

    role_result = await UserRoleAllocation.get_user_role_by_user_id(user_id, db)
    role_name = role_result.role_name or "EMPLOYEE"

    org_result = await UserOrganizationRepository.get_user_organization_by_user_id(user_id, db)
    org_id = org_result.organization_id

    new_payload = Security.build_token_payload(user.user_id, user.user_email, org_id, role_name)
    return TokenResponse(
        access_token=Security.create_access_token(new_payload),
        refresh_token=Security.create_refresh_token(new_payload),
    )
