from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=255)
    user_email: EmailStr
    user_password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    user_email: EmailStr
    user_password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class MessageResponse(BaseModel):
    message: str
