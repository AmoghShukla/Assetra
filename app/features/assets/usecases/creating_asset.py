import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.features.assets.repository import AssetRepository
from app.models import Asset, AssetType
from app.models.user import User
from app.utilities.enums import AssetStatus
from app.utilities.exceptions import ConflictException, NotFoundException, ForbiddenException, InvalidAssetCodeException
from app.features.assets.schemas import CreateAssetRequest, AssetResponse, ASSET_CODE_REGEX
from app.utilities.permission import resolve_user_permissions


async def create_assets(data: CreateAssetRequest, current_user: User, db: AsyncSession) -> AssetResponse:
    perms = await resolve_user_permissions(current_user.user_id, db)
    if "asset:create" not in perms:
        raise ForbiddenException("You do not have permission to create assets")
    
    if not re.match(ASSET_CODE_REGEX, data.asset_code):
        raise InvalidAssetCodeException()

    type_result = await AssetRepository.get_asset_types_by_type_and_organization_id(data.asset_type_id, current_user._organization_id, db)
    if not type_result:
        raise NotFoundException("Asset type not found in your organization")

    existing = await AssetRepository.get_asset_by_code(data.asset_code, db)
    if existing:
        raise ConflictException(f"Asset code {data.asset_code} already exists")

    asset = Asset(
        asset_type_id=data.asset_type_id,
        asset_code=data.asset_code,
        asset_description=data.asset_description,
        asset_status=AssetStatus.AVAILABLE,
        organization_id=current_user._organization_id,
        updated_by=current_user.user_id,
    )
    result = await AssetRepository.create_asset_type(asset, db)
    return result
