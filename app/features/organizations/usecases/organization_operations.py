from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.features.auth.schemas import MessageResponse
from app.features.organizations.repository import OrganizationRepository
from app.models.organization import Organization
from app.utilities.exceptions import NotFoundException
from app.features.organizations.schemas import UpdateOrganizationRequest, OrganizationResponse
from app.features.organizations.repository import OrganizationRepository

async def update_organization(org_id: UUID, data: UpdateOrganizationRequest, db: AsyncSession) -> OrganizationResponse:
    result = await OrganizationRepository.get_organization_by_id(org_id, db)
    if not result:
        raise NotFoundException("Organization")

    result.organization_name = data.organization_name
    org = await OrganizationRepository.create_organization(result, db)
    return OrganizationResponse.model_validate(org)


async def delete_organization(org_id: UUID, db: AsyncSession) -> dict:
    result = await db.execute(select(Organization).where(Organization.organization_id == org_id, Organization.is_deleted == False))
    org = result.scalar_one_or_none()
    if not org:
        raise NotFoundException("Organization")

    org.is_deleted = True
    deletion = await OrganizationRepository.delete_organization(org, db)
    return deletion


async def get_organization(org_id: UUID, db: AsyncSession):
    org = await OrganizationRepository.get_organization_by_id(org_id, db)
    if not org:
        raise NotFoundException("Organization")
    return OrganizationResponse.model_validate(org)


async def list_all_organizations(db: AsyncSession) -> List[OrganizationResponse]:
    organizations = await OrganizationRepository.get_all_organization(db)
    return [OrganizationResponse.model_validate(org) for org in organizations]
