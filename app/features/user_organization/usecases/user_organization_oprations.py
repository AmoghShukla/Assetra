from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.features.organizations.usecases.organization_operations import get_organization
from app.features.users.usecases.get_user import get_user_by_id
from app.models.user_organization import UserOrganization
from app.utilities.exceptions import ConflictException, NotFoundException
from app.features.user_organization.repository import UserOrganizationRepository
from app.utilities.session import get_db

async def get_users_by_organization_id(organization_id, db : AsyncSession):
    organization = await get_organization(organization_id, db)
    if not organization:
        raise ConflictException("Organization not found")
    return await UserOrganizationRepository.get_user_by_organization(organization_id, db)
    