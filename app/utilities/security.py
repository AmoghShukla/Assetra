from datetime import datetime, UTC, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from .exceptions import NotFoundException, ConflictException, BadRequestException

from app.utilities.config import settings

PasswordContext : PasswordHash = PasswordHash.recommended()

class Security:

    @staticmethod
    def build_token_payload(user_id, user_email, organization_id, role):
        return {
            "sub": str(user_id),
            "user_email": user_email,
            "organization_id": str(organization_id) if organization_id else None,
            "role": role,
        }

    @staticmethod
    def hash_password(password : str):
        try:
            return PasswordContext.hash(password)
        except Exception as e:
            raise BadRequestException("Error While Hashing the Password")
        
    @staticmethod
    def verify_password(plain_password, hashed_password):
        try:
            return PasswordContext.verify(plain_password, hashed_password)
        except Exception as e:
            raise BadRequestException("Error While Verifying the Password")
        
    @staticmethod
    def create_access_token(data : dict):
        try:
            data_to_encode = data.copy()
            expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

            data_to_encode.update({'exp' : expiry, 'type' : "access"})
            return jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except jwt.PyJWKError as e:
            raise BadRequestException("Error While Creating the Access Token!!")

    @staticmethod
    def create_refresh_token(data : dict):
        try:
            data_to_encode = data.copy()
            expiry = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

            data_to_encode.update({'exp' : expiry, 'type' : "refresh"})
            return jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except jwt.PyJWKError as e:
            raise BadRequestException("Error While Creating the Refresh Token!!")

    @staticmethod
    def decode_token(token):
        new_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not new_token:
            raise BadRequestException("Error while decoding the token")
        return new_token