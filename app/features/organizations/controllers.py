from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.utilities.session import get_db
from app.utilities.enums import RoleName
from app.utilities.dependencies import get_current_user, require_roles
from app.features.organizations.schemas import (
    CreateOrganizationRequest, UpdateOrganizationRequest, OrganizationResponse
)
from app.features.organizations.usecases.create_organization import create_organization
from app.features.organizations.usecases.organization_operations import (
    update_organization, delete_organization, get_organization, list_all_organizations
)
from app.features.organizations.usecases.organization_operations import get_organization

router = APIRouter(prefix="/organizations", tags=["Organizations"])

superadmin_only = require_roles(RoleName.SUPERADMIN)
superadmin_or_org_admin = require_roles(RoleName.SUPERADMIN, RoleName.ORG_ADMIN)


@router.post("/create_org", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: CreateOrganizationRequest,
    _=Depends(superadmin_only),
    db: AsyncSession = Depends(get_db),
):
    return await create_organization(data, db)


@router.get("/list_organizations", response_model=List[OrganizationResponse])
async def list_organizations(_=Depends(superadmin_only), db: AsyncSession = Depends(get_db)):
    return await list_all_organizations(db)


@router.get("/get_organization_by_id/{organizations_id}", response_model=OrganizationResponse)
async def get_organization_by_id(organizations_id: UUID, _=Depends(superadmin_or_org_admin), db: AsyncSession = Depends(get_db)):
    organization = await get_organization(organizations_id, db)
    return organization


@router.put("/update_organizations/{organizations_id}", response_model=OrganizationResponse)
async def update_organizations(
    organizations_id: UUID,
    data: UpdateOrganizationRequest,
    _=Depends(superadmin_or_org_admin),
    db: AsyncSession = Depends(get_db),
):
    return await update_organization(organizations_id, data, db)


@router.delete("/delete_organizations/{organizations_id}")
async def delete_organizations(organizations_id: UUID,  _=Depends(superadmin_only), db: AsyncSession = Depends(get_db)):
    return await delete_organization(organizations_id, db)
