from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.user_organization.schema import CreateUserOrganization, UserOrganizationResponse
from app.utilities.dependencies import require_roles
from app.utilities.enums import RoleName
from app.utilities.session import get_db
from app.features.user_organization.usecases.create_user_organization import create_user_organization_allocation 
from app.features.user_organization.usecases.user_organization_oprations import get_users_by_organization_id

router = APIRouter(prefix="/user_organization", tags=["User_Organization"])

org_admin_up = require_roles(RoleName.SUPERADMIN, RoleName.ORG_ADMIN)
superadmin_only = require_roles(RoleName.SUPERADMIN)


@router.post('/create_user_organization', response_model=UserOrganizationResponse)
async def create_user_organization(payload : CreateUserOrganization,_=Depends(org_admin_up),  db : AsyncSession = Depends(get_db)):
    return await create_user_organization_allocation(payload, db)

@router.get('/get_users_by_organization', response_model=List[UserOrganizationResponse])
async def get_users_by_organization(organization_id : UUID, _=Depends(org_admin_up), db : AsyncSession = Depends(get_db)):
    return await get_users_by_organization_id(organization_id, db)