from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.features.user_organization.repository import UserOrganizationRepository
from app.features.user_role.repository import UserRoleAllocation
from app.features.user_role.usecases.get_user_role import get_user_role_by_user_id
from app.models import User, UserOrganization, UserRole, Role
from app.utilities.security import Security
from app.utilities.exceptions import UnauthorizedException
from app.features.auth.schemas import LoginRequest, TokenResponse
from app.features.users.repository import UserRepository


async def user_login(data, db: AsyncSession) -> TokenResponse:
    user_email = data.username
    user_password = data.password
    user = await UserRepository.get_user_by_email(user_email, db)

    if not user or not Security.verify_password(user_password, user.user_password):
        raise UnauthorizedException("Invalid email or password")

    role_result = await UserRoleAllocation.get_user_role_by_user_id(user.user_id, db)
    role_name = role_result.role_name or "EMPLOYEE"

    org_result = await UserOrganizationRepository.get_user_organization_by_user_id(user.user_id, db)
    org_id = org_result.organization_id

    payload = Security.build_token_payload(user.user_id, user.user_email, org_id, role_name)
    return TokenResponse(
        access_token=Security.create_access_token(payload),
        refresh_token=Security.create_refresh_token(payload),
    )
