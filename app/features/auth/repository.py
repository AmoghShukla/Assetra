from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.schemas import MessageResponse
from app.models.user import User
from app.utilities.exceptions import DatabaseError


class AuthRepository:
        
    @staticmethod
    async def change_password(user, db: AsyncSession):
        try:
            db.add(user) 
            await db.commit()
            return {"message": "Password has been changed successfully!!"}
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError()
        
    @staticmethod
    async def signup(data, db):
        try:
            db.add(data)
            await db.flush()     
            await db.refresh(data) 
            return data          
        except SQLAlchemyError as e:
            await db.rollback() 
            raise DatabaseError()
