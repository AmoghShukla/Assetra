from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Asset, AssetAssignment, User, UserOrganization
from app.utilities.enums import AssetStatus
from app.utilities.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.features.assets.schemas import AssignAssetRequest
from app.features.assets.repository import AssetAssignmentRepository, AssetRepository
from app.utilities.permission import resolve_user_permissions


async def assign_asset(asset_id: UUID, data: AssignAssetRequest, current_user: User, db: AsyncSession) -> dict:
    perms = await resolve_user_permissions(current_user.user_id, db)
    if "asset:assign" not in perms:
        raise ForbiddenException("You do not have permission to assign assets")
    
    asset = await _get_org_asset(asset_id, current_user._organization_id, db)

    if asset.asset_status != AssetStatus.AVAILABLE:
        raise BadRequestException("Only AVAILABLE assets can be assigned")

    ''' Check whether the user belongs to the right organization'''
    employee_organization = await AssetRepository.get_employee_by_organization_id(data.employee_id, current_user._organization_id, db)
    if not employee_organization:
        raise NotFoundException("Employee not found in your organization")

    changed_assest_status = await AssetRepository.change_asset_status(asset, AssetStatus.ALLOCATED, current_user.user_id, db)

    assignment = AssetAssignment(
        asset_id=asset_id,
        assigned_to=data.employee_id,
        assigned_by=current_user.user_id,
    )
    assignment_created = await AssetAssignmentRepository.create_asset_assignment(assignment, db)
    return {"message": "Asset assigned successfully"}


async def unassign_asset(asset_id: UUID, current_user: User, db: AsyncSession) -> dict:  
    perms = await resolve_user_permissions(current_user.user_id, db)
    if "asset:unassign" not in perms:
        raise ForbiddenException("You do not have permission to unassign assets")

    asset = await _get_org_asset(asset_id, current_user._organization_id, db)

    if asset.asset_status != AssetStatus.ALLOCATED:
        raise BadRequestException("Only ALLOCATED assets can be unassigned")

    assignment = await AssetAssignmentRepository.get_asset_assignment_with_asset_id(asset_id, db)
    if assignment:
        await AssetAssignmentRepository.soft_delete_asset_assignment(assignment, db)

    changed_status_of_assignment = await AssetAssignmentRepository.change_asset_assignment_status(asset, AssetStatus.AVAILABLE, current_user.user_id, db)
    return {"message": "Asset unassigned successfully"}


async def _get_org_asset(asset_id: UUID, org_id: UUID, db: AsyncSession) -> Asset:
    result = await AssetRepository.get_org_asset(asset_id, org_id, db)
    if not result:
        raise NotFoundException("Asset")
    return result
