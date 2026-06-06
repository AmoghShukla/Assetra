from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utilities.security import Security
from app.utilities.exceptions import BadRequestException
from app.features.auth.schemas import ChangePasswordRequest, MessageResponse
from ..repository import AuthRepository


async def change_password(payload: ChangePasswordRequest, current_user: User, db: AsyncSession) -> MessageResponse:
    if not Security.verify_password(payload.current_password, current_user.user_password):
        raise BadRequestException("Current password is incorrect")

    if payload.current_password == payload.new_password:
        raise BadRequestException("New password must differ from current password")

    current_user.user_password = Security.hash_password(payload.new_password)

    response_data = await AuthRepository.change_password(current_user, db)

    return MessageResponse(message=response_data["message"])
