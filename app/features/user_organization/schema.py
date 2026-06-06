from uuid import UUID

from pydantic import BaseModel


class CreateUserOrganization(BaseModel):
    user_id : UUID
    organization_id : UUID

class UserOrganizationResponse(BaseModel):
    user_organization_id : UUID
    user_id : UUID
    organization_id : UUID