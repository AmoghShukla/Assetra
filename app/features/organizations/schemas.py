from uuid import UUID

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CreateOrganizationRequest(BaseModel):
    organization_name: str = Field(..., min_length=2, max_length=255)


class UpdateOrganizationRequest(BaseModel):
    organization_name: str = Field(..., min_length=2, max_length=255)


class OrganizationResponse(BaseModel):
    organization_id: UUID
    organization_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
