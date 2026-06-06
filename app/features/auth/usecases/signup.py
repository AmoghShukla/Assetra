from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.features.auth.repository import AuthRepository
from app.features.user_role.schemas import CreateUserRole
from app.models.user import User
from app.features.users import UserRepository
from app.features.role.usecases.get_role import get_role_by_name
from app.utilities.security import Security
from app.utilities.exceptions import ConflictException
from app.utilities.enums import RoleName
from app.features.auth.schemas import SignupRequest, TokenResponse
from app.features.user_role.repository import UserRoleAllocation

async def user_signup(data: SignupRequest, db: AsyncSession):
    '''checking whether the entered email is unique or not'''
    user_exists = await UserRepository.get_user_by_email(data.user_email, db)
    if user_exists:
        raise ConflictException("Email already registered")

    '''creating new user'''
    new_user = User(
        user_name = data.user_name,
        user_email = data.user_email,
        user_password = Security.hash_password(data.user_password)
    )
    new_user = await AuthRepository.signup(new_user, db)

    '''Adding to the UserRole Table '''
    new_user_role = await get_role_by_name(RoleName.EMPLOYEE.value, db)
    payload = CreateUserRole(
        user_id=new_user.user_id,
        role_id=new_user_role.role_id,
    )
    allocation = await UserRoleAllocation.create_user_role(payload, db)
    return {'message' : 'User Created Successfully!!!'}
    
    
