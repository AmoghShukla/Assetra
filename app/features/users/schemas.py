from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    user_id: UUID
    user_name: str
    user_email: str
    created_at: datetime

    model_config = {"from_attributes": True}

class UserPermissionsResponse(BaseModel):
    user_id: UUID
    role: str
    permissions: List[str]


class RevokePermissionRequest(BaseModel):
    permission_name: str
    reason: Optional[str] = None


class UpdateUserRequest(BaseModel):
    user_name: Optional[str] = Field(min_length=2, max_length=255)