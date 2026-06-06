from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.features.assets.repository import AssetRepository
from app.utilities.permission import resolve_user_permissions
from app.models import Asset, AssetType, AssetAssignment,  User
from app.utilities.enums import AssetStatus, RoleName
from app.utilities.exceptions import ConflictException, NotFoundException, ForbiddenException
from app.features.assets.schemas import (
    UpdateAssetRequest, AssetResponse, ChangeAssetStatusRequest, AssetMetricsResponse,
    CreateAssetTypeRequest, AssetTypeResponse,
)

'''-----------------------------  Assets  -------------------------------------'''

async def update_asset(asset_id: UUID, data: UpdateAssetRequest, current_user: User, db: AsyncSession) -> AssetResponse:
    perms = await resolve_user_permissions(current_user.user_id, db)
    if "asset:update" not in perms:
        raise ForbiddenException("You do not have permission to update assets")
    
    asset = await AssetRepository.get_org_asset(asset_id, current_user._organization_id, db)
    if not asset:
        raise NotFoundException("Asset")
    updated_asset = AssetRepository.update_asset(data, asset, current_user, db)
    return AssetResponse.model_validate(updated_asset)


async def change_asset_status(asset_id: UUID, data: ChangeAssetStatusRequest, current_user: User, db: AsyncSession) -> AssetResponse:
    perms = await resolve_user_permissions(current_user.user_id, db)
    if "asset:update" not in perms:
        raise ForbiddenException("You do not have permission to change asset status")
    
    asset = await AssetRepository.get_org_asset(asset_id, current_user._organization_id, db)
    if not asset:
        raise NotFoundException("Asset")

    result = await AssetRepository.change_asset_status(asset, data.status, current_user.user_id, db)
    return AssetResponse.model_validate(result)


async def delete_asset(asset_id: UUID, current_user: User, db: AsyncSession) -> dict:
    perms = await resolve_user_permissions(current_user.user_id, db)
    if "asset:delete" not in perms:
        raise ForbiddenException("You do not have permission to delete assets")
    
    asset = await AssetRepository.get_org_asset(asset_id, current_user._organization_id, db)
    if not asset:
        raise NotFoundException("Asset")
    return await AssetRepository.delete_asset(asset, db)


async def get_asset_metrics(current_user: User, db: AsyncSession) -> AssetMetricsResponse:
    rows = await AssetRepository.get_asset_metrics(current_user, db)
    counts = {row[0]: row[1] for row in rows}

    available = counts.get(AssetStatus.AVAILABLE, 0)
    allocated = counts.get(AssetStatus.ALLOCATED, 0)
    under_maintenance = counts.get(AssetStatus.UNDER_MAINTENANCE, 0)
    retired = counts.get(AssetStatus.RETIRED, 0)
    return AssetMetricsResponse(
        available=available,
        allocated=allocated,
        under_maintenance=under_maintenance,
        retired=retired,
        total=available + allocated + under_maintenance + retired,
    )


async def list_assets(current_user: User, db: AsyncSession) -> List[AssetResponse]:
    result = await AssetRepository.get_alloted_assests(current_user, db)
    return [AssetResponse.model_validate(a) for a in result]



'''-----------------------AssetType-------------------------------'''



async def create_asset_type(
        data: CreateAssetTypeRequest, 
        current_user: User, 
        db: AsyncSession
    ) -> AssetTypeResponse:
    exists = await AssetRepository.get_asset_types_by_name(data.asset_name, data.organization_id, db)
    if exists:
        raise ConflictException('Asset Already Exists for your organization!!!!')
    else:
        asset_type = AssetType(
            asset_name=data.asset_name,
            organization_id = current_user._organization_id
        )
        return await AssetRepository.create_asset_type(asset_type, db)


async def list_asset_types(current_user: User, db: AsyncSession):
    result = await AssetRepository.get_all_asset_types_by_organization_id(current_user._organization_id, db)
    return result
