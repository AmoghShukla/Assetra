from sqlalchemy.ext.asyncio import AsyncSession

from app.features.organizations.usecases.organization_operations import get_organization
from app.features.users.usecases.get_user import get_user_by_id
from app.models.user_organization import UserOrganization
from app.utilities.exceptions import ConflictException, NotFoundException
from app.features.user_organization.repository import UserOrganizationRepository


async def create_user_organization_allocation(payload, db : AsyncSession):
    user = await get_user_by_id(payload.user_id, db)
    if not user:
        raise NotFoundException('User')
    
    organization = await get_organization(payload.organization_id, db)
    if not organization:
        raise NotFoundException('Organization')
    
    allocation_check_one = await UserOrganizationRepository.already_allocated_user_organization(payload.user_id, payload.organization_id, db)
    
    allocation_check_two = await UserOrganizationRepository.get_user_organization_by_user_id(payload.user_id, db)
    
    if allocation_check_one or allocation_check_two:
        raise ConflictException(f'An Allocation for user with id : {payload.user_id} Already Exists!!')
    else:
        allocation = UserOrganization(
            user_id = payload.user_id,
            organization_id = payload.organization_id
        )

    user_organization = await UserOrganizationRepository.create_user_organization(allocation, db)
    
    return user_organization
    