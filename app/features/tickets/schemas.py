from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utilities.enums import TicketStatus, TICKET_MAX_DESCRIPTION_LENGTH


class CreateTicketRequest(BaseModel):
    asset_type_id: UUID
    ticket_title: str = Field(..., min_length=2, max_length=255)
    ticket_description: Optional[str] = Field(None, max_length=TICKET_MAX_DESCRIPTION_LENGTH)


class UpdateTicketStatusRequest(BaseModel):
    status: TicketStatus


class TicketResponse(BaseModel):
    ticket_id: UUID
    organization_id: UUID
    employee_id: UUID
    asset_type_id: UUID
    ticket_title: str
    ticket_description: Optional[str]
    ticket_status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
