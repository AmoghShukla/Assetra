from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.features.assets.repository import AssetRepository
from app.features.tickets.repository import TicketRepository
from app.models import Ticket, AssetType, User
from app.utilities.enums import TicketStatus, TICKET_TRANSITIONS, RoleName
from app.utilities.exceptions import NotFoundException, ForbiddenException, BadRequestException, InvalidTicketTransitionException
from app.features.tickets.schemas import CreateTicketRequest, UpdateTicketStatusRequest, TicketResponse


async def create_ticket(data: CreateTicketRequest, current_user: User, db: AsyncSession) -> TicketResponse:
    if current_user._role != RoleName.EMPLOYEE.value:
        raise ForbiddenException("Only employees can raise asset requests")

    asset_type = await AssetRepository.get_asset_types_by_type_and_organization_id(data.asset_type_id, current_user._organization_id, db)
    if not asset_type:
        raise NotFoundException("Asset type not defined in your organization")

    ticket = Ticket(
        organization_id=current_user._organization_id,
        employee_id=current_user.user_id,
        asset_type_id=data.asset_type_id,
        ticket_title=data.ticket_title,
        ticket_description=data.ticket_description,
        ticket_status=TicketStatus.TODO,
    )
    return await TicketRepository.create_ticket(ticket, db)


async def update_ticket_status(
    ticket_id: UUID,
    status,
    current_user: User,
    db: AsyncSession,
) -> TicketResponse:
    ticket = await TicketRepository.get_ticket_by_ticket_organization_id(ticket_id, current_user._organization_id, db)
    if not ticket:
        raise NotFoundException("Ticket")

    current_status = TicketStatus(ticket.ticket_status)
    allowed_transitions = TICKET_TRANSITIONS.get(current_status, [])

    if status not in allowed_transitions:
        raise InvalidTicketTransitionException(current_status.value, status.value)

    updated_ticket = await TicketRepository.update_ticket_status(ticket, status, current_user.user_id, db)
    return TicketResponse.model_validate(updated_ticket)


async def get_tickets(current_user: User, db: AsyncSession) -> List[TicketResponse]:
    if current_user._role == RoleName.EMPLOYEE.value:
        result = await TicketRepository.get_ticket_by_employee_id(current_user.user_id, db)
    else:
        result = await TicketRepository.get_ticket_by_organization_id(current_user._organization_id, db)

    return [TicketResponse.model_validate(t) for t in result]


async def resolve_ticket(ticket_id: UUID, current_user: User, db: AsyncSession) -> TicketResponse:
    return await update_ticket_status(
        ticket_id,
        UpdateTicketStatusRequest(status=TicketStatus.RESOLVED),
        current_user,
        db
    )
