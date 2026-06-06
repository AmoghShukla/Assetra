from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.features.organizations.repository import OrganizationRepository
from app.models.organization import Organization
from app.utilities.exceptions import ConflictException, NotFoundException
from app.features.organizations.schemas import CreateOrganizationRequest, OrganizationResponse


async def create_organization(data: CreateOrganizationRequest, db: AsyncSession) -> OrganizationResponse:
    existing = await OrganizationRepository.get_organization_by_name(data.organization_name, db)
    if existing:
        raise ConflictException("Organization name already exists")

    org = Organization(organization_name=data.organization_name)
    org = OrganizationRepository.create_organization(org, db)
    return OrganizationResponse.model_validate(org)
