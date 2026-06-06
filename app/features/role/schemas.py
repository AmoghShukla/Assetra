from uuid import UUID

from pydantic import BaseModel
from app.utilities.enums import RoleName

class RoleResponse(BaseModel):
    role_id : UUID
    role_name : str
