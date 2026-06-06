from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.utilities.enums import RoleName, TicketStatus
from app.utilities.session import get_db
from app.utilities.dependencies import get_current_user
from app.features.tickets.schemas import CreateTicketRequest, UpdateTicketStatusRequest, TicketResponse
from app.features.tickets.usecases import ticket_ops
from app.utilities.dependencies import require_roles

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/create_ticket", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    data: CreateTicketRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ticket_ops.create_ticket(data, current_user, db)


@router.get("/get_all_tickets", response_model=List[TicketResponse])
async def get_all_tickets(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ticket_ops.get_tickets(current_user, db)


@router.patch("/update_ticket_status/{ticket_id}", response_model=TicketResponse)
async def update_ticket_status(
    ticket_id: UUID,
    status: TicketStatus,
    _=Depends(require_roles(RoleName.IT_ADMIN.value, RoleName.ORG_ADMIN.value, RoleName.SUPERADMIN.value)),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ticket_ops.update_ticket_status(ticket_id, status, current_user, db)


@router.post("/resolve/{ticket_id}", response_model=TicketResponse)
async def resolve_ticket_route(
    ticket_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ticket_ops.resolve_ticket(ticket_id, current_user, db)
