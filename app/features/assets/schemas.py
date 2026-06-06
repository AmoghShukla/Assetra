from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.utilities.enums import AssetStatus
import re

ASSET_CODE_REGEX = r"^[A-Z]{1}[0-9]{4}$"


class CreateAssetTypeRequest(BaseModel):
    asset_name: str = Field(..., min_length=2, max_length=255)
    organization_id : UUID


class AssetTypeResponse(BaseModel):
    asset_type_id: UUID
    asset_name: str
    organization_id: UUID

    model_config = {"from_attributes": True}


class CreateAssetRequest(BaseModel):
    asset_type_id: UUID
    asset_code: str
    asset_description: Optional[str] = None

    @field_validator("asset_code")
    @classmethod
    def validate_asset_code(cls, v: str) -> str:
        if not re.match(ASSET_CODE_REGEX, v):
            raise ValueError("Asset code must be 1 uppercase letter followed by 4 digits (e.g. A1234)")
        return v


class UpdateAssetRequest(BaseModel):
    asset_name: Optional[str] = Field(None, min_length=2, max_length=255)
    asset_description: Optional[str] = None


class ChangeAssetStatusRequest(BaseModel):
    status: AssetStatus


class AssignAssetRequest(BaseModel):
    employee_id: UUID


class AssetResponse(BaseModel):
    asset_id: UUID
    asset_code: str
    asset_description: Optional[str]
    asset_status: str
    asset_type_id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssetMetricsResponse(BaseModel):
    available: int
    allocated: int
    under_maintenance: int
    retired: int
    total: int
