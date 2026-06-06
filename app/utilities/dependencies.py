from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.features.users import UserRepository
from app.utilities.session import get_db
from app.utilities.security import Security
from app.utilities.exceptions import UnauthorizedException, ForbiddenException
from app.utilities.enums import RoleName
from app.features.role.repository import GetRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    payload = Security.decode_token(token)
    if not payload:
        raise UnauthorizedException("Invalid Token!!!") 
        
    if payload.get("type") != "access":
        raise UnauthorizedException("Invalid token type")

    user_id = payload.get('sub')
    user = await UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise UnauthorizedException("User not found")

    if not user.user_roles:
        raise UnauthorizedException("User has no assigned roles")

    first_role_allocation = user.user_roles[0]

    user_role_obj = await GetRole.get_role_by_id(
        first_role_allocation.role_id, 
        db
    )
    
    if not user_role_obj:
        raise UnauthorizedException("Assigned role does not exist")

    user._role = user_role_obj.role_name
    user._organization_id = payload.get("organization_id")
    
    return user



def require_roles(*roles: RoleName):
    async def checker(current_user=Depends(get_current_user)):
        if current_user._role not in [r for r in roles]:
            raise ForbiddenException(f"Unauthoized!! Required role: {[r for r in roles]}")
        return current_user
    return checker
