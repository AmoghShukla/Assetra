from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.utilities.session import get_db
from app.utilities.enums import RoleName
from app.utilities.dependencies import get_current_user, require_roles
from app.features.assets.schemas import (
    CreateAssetRequest, UpdateAssetRequest, AssetResponse, ChangeAssetStatusRequest,
    AssignAssetRequest, AssetMetricsResponse, CreateAssetTypeRequest, AssetTypeResponse,
)
# from app.features.assets.usecases
from app.features.assets.usecases.creating_asset import create_assets
from app.features.assets.usecases.assign_asset import assign_asset, unassign_asset
from app.features.assets.usecases.asset_ops import (
    update_asset, change_asset_status, delete_asset, get_asset_metrics,
    list_assets, create_asset_type, list_asset_types,
)

router = APIRouter(prefix="/assets", tags=["Assets"])

org_admin_up = require_roles(RoleName.SUPERADMIN, RoleName.ORG_ADMIN)


'''----------------------------Asset Types---------------------------------------'''
@router.post("/create_asset_types",response_model=AssetTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_asset_types(
    data: CreateAssetTypeRequest,
    current_user=Depends(get_current_user),
    _=Depends(org_admin_up),
    db: AsyncSession = Depends(get_db),
):
    return await create_asset_type(data, current_user, db)


@router.get("/get_asset_types", response_model=List[AssetTypeResponse])
async def get_asset_types(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await list_asset_types(current_user, db)

        
'''---------------------------- Assets ----------------------------------------'''


@router.get("/get_asset_metrics", response_model=AssetMetricsResponse)
async def asset_metrics(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_asset_metrics(current_user, db)


@router.post("/create_asset", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def creating_asset(
    data: CreateAssetRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_assets(data, current_user, db)


@router.get("/get_allotted_assets", response_model=List[AssetResponse])
async def get_allotted_assets(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await list_assets(current_user, db)


@router.put("/update_asset", response_model=AssetResponse)
async def update__asset(
    asset_id: UUID,
    data: UpdateAssetRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await update_asset(asset_id, data, current_user, db)


@router.patch("/change_status", response_model=AssetResponse)
async def change_status(
    asset_id: UUID,
    data: ChangeAssetStatusRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await change_asset_status(asset_id, data, current_user, db)


@router.delete("/delete_asset/{asset_id}")
async def delete_org_asset(
    asset_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await delete_asset(asset_id, current_user, db)



''' ----------------------------Asset_Assignment--------------------------------------'''
assignment_router = APIRouter(prefix="/assets_assignment", tags=["Assets_Assignment"])

@assignment_router.post("/{asset_id}/assign")
async def assign_asset_route(
    asset_id: UUID,
    data: AssignAssetRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await assign_asset(asset_id, data, current_user, db)


@assignment_router.post("/{asset_id}/unassign")
async def unassign_asset_route(
    asset_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await unassign_asset(asset_id, current_user, db)
