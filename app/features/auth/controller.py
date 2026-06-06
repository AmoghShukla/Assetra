from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.usecases import refresh_token
from app.features.auth.usecases.login import user_login
from app.features.auth.usecases.signup import user_signup
from app.utilities.session import get_db
from app.features.auth.schemas import ChangePasswordRequest, LoginRequest, MessageResponse, RefreshTokenRequest, SignupRequest, TokenResponse
from app.utilities.dependencies import get_current_user
from app.features.auth.usecases import change_user_password


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=201)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await user_signup(data, db)

@router.post("/login", response_model=TokenResponse)
async def login(data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await user_login(data, db)

@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    data: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await change_user_password.change_password(data, current_user, db)

@router.post("/refresh_token_regeneration", response_model=TokenResponse)
async def refresh_token_regeneration(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    return await refresh_token(data, db)