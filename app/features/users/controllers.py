from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status 
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.users.usecases import get_user
from app.features.users.usecases.get_permissions import get_user_permissions
from app.features.users.usecases.user_operations import delete_user, restore_it_admin_asset_permission, revoke_it_admin_asset_permission, update_user
from app.utilities.dependencies import get_current_user, require_roles
from app.utilities.enums import RoleName
from app.utilities.session import get_db
from app.features.users.schemas import RevokePermissionRequest, UpdateUserRequest, UserPermissionsResponse, UserResponse

router = APIRouter(prefix="/user", tags=["User"])

org_admin_up = require_roles(RoleName.SUPERADMIN.value, RoleName.ORG_ADMIN.value)
superadmin_only = require_roles(RoleName.SUPERADMIN)

@router.get("/get_user_by_id", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_user.get_user_by_id(user_id, db)

@router.get("/get_user_by_email", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_email(user_email: EmailStr, db: AsyncSession = Depends(get_db)):
    return await get_user.get_user_by_email(user_email, db)

@router.get("/get_users", response_model=List[UserResponse])
async def get_users(current_user=Depends(org_admin_up), db: AsyncSession = Depends(get_db)):
    return await get_user.list_users(current_user, db)

@router.get("/{user_id}/permissions", response_model=UserPermissionsResponse)
async def get_permissions_route(
    user_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_user_permissions(user_id, current_user, db)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_route(
    user_id: UUID,
    data: UpdateUserRequest,
    current_user=Depends(org_admin_up),
    db: AsyncSession = Depends(get_db),
):
    return await update_user(user_id, data, current_user, db)


@router.delete("/{user_id}")
async def delete_user_route(
    user_id: UUID,
    current_user=Depends(org_admin_up),
    db: AsyncSession = Depends(get_db),
):
    return await delete_user(user_id, current_user, db)


@router.post("/{user_id}/revoke-asset-permissions")
async def revoke_asset_permissions(
    user_id: UUID,
    data: RevokePermissionRequest,
    current_user=Depends(superadmin_only),
    db: AsyncSession = Depends(get_db),
):
    return await revoke_it_admin_asset_permission(user_id, data.reason or "", current_user, db)


@router.post("restore-asset-permissions/{user_id}")
async def restore_asset_permissions(
    user_id: UUID,
    current_user=Depends(superadmin_only),
    db: AsyncSession = Depends(get_db),
):
    return await restore_it_admin_asset_permission(user_id, current_user, db)
