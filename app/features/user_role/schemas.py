from uuid import UUID
from pydantic import BaseModel


class CreateUserRole(BaseModel):
    user_id : UUID
    role_id : UUID

class UserRoleResponse(BaseModel):
    user_id : UUID
    role_id : UUID
    role_name : str
