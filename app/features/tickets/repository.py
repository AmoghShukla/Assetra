

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.features.tickets.schemas import TicketResponse
from app.models.ticket import Ticket
from app.utilities.exceptions import DatabaseError


class TicketRepository:

    @staticmethod
    async def create_ticket(ticket, db):
        try:
            db.add(ticket)
            await db.flush()
            await db.refresh(ticket)
            return TicketResponse.model_validate(ticket)
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_ticket_by_ticket_organization_id(ticket_id, organization_id, db):
        try:
            statement = (
                select(Ticket)
                .where(
                    Ticket.ticket_id == ticket_id,
                    Ticket.organization_id == organization_id,
                    Ticket.is_deleted == False
                    )
                )
            result = await db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_ticket_by_employee_id(employee_id, db):
        try:
            statement = (
                select(Ticket)
                .where(
                    Ticket.employee_id == employee_id,
                    Ticket.is_deleted == False
                    )
                )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()
    
    @staticmethod
    async def get_ticket_by_organization_id(organization_id, db):
        try:
            statement = (
                select(Ticket)
                .where(
                    Ticket.organization_id == organization_id,
                    Ticket.is_deleted == False
                    )
                )
            result = await db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError()
    

    @staticmethod
    async def update_ticket_status(ticket, status, user_id, db):
        try:
            ticket.ticket_status = status
            ticket.updated_by = user_id
            db.add(ticket)
            await db.flush()
            await db.refresh(ticket)
        except SQLAlchemyError as e:
            raise DatabaseError()