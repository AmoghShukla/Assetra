from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.users.schemas import UserResponse
from app.models.user import User
from app.utilities.exceptions import NotFoundException
from app.features.users.repository import UserRepository


async def get_user_by_id(user_id : UUID, db : AsyncSession):
    user = await UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise NotFoundException(f'User with user_id : {user_id}')
    return user

async def get_user_by_email(user_email : str, db : AsyncSession):
    user = await UserRepository.get_user_by_email(user_email, db)
    if not user:
        raise NotFoundException(f'User with email : {user_email}')
    return user

async def list_users(current_user: User, db: AsyncSession) -> List[UserResponse]:
    """Lists all the users in the same organization."""
    organization_id = current_user._organization_id
    if not organization_id:
        return []

    users = await UserRepository.get_all_users(organization_id, db)
    return [UserResponse.model_validate(user) for user in users]
