from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.role.schemas import RoleResponse
from app.utilities.enums import RoleName
from app.utilities.session import get_db
from .usecases import get_role
from app.features.auth.schemas import ChangePasswordRequest, MessageResponse
from app.utilities.dependencies import get_current_user, require_roles
from app.features.auth.usecases.change_user_password import change_password


router = APIRouter(prefix="/role", tags=["Role"])

org_admin_up = require_roles(RoleName.SUPERADMIN, RoleName.ORG_ADMIN)
superadmin_only = require_roles(RoleName.SUPERADMIN)


@router.get("/get_role_by_id", response_model=RoleResponse)
async def get_role_by_role_id(
    role_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_role.get_role_by_id(role_id, db)

@router.get('/get_role_by_name', response_model=RoleResponse)
async def get_role_by_name(
    role_name : RoleName,
    _=Depends(org_admin_up),
    db : AsyncSession = Depends(get_db)
):
    return await get_role.get_role_by_name(role_name, db)

@router.get('/get_all_roles', response_model=List[RoleResponse])
async def get_all_roles(
    db : AsyncSession = Depends(get_db),
    _=Depends(org_admin_up)
):
    return await get_role.get_all_roles(db)