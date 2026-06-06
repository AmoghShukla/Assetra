from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.user_role.usecases import get_user_role
from app.features.user_role.schemas import CreateUserRole, UserRoleResponse
from app.features.user_role.usecases.create_user_role import create_intermediate_user_role
from app.utilities.session import get_db

router = APIRouter(prefix='/user_role', tags=['User_Role'])

@router.post("/create_user_role", response_model=UserRoleResponse)
async def create_user_role(
    payload : CreateUserRole,
    db : AsyncSession = Depends(get_db)    
):
    return await create_intermediate_user_role(payload, db)

@router.get('/get_user_role_by_user_id', response_model=UserRoleResponse)
async def get_user_role_by_user_id(
    user_id : UUID, 
    db : AsyncSession = Depends(get_db)
):
    return await get_user_role.get_user_role_by_user_id(user_id, db)
    