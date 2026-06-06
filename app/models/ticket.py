from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities.audit_trail_mixin import AuditTrailMixin
from app.utilities.base import Base
from datetime import datetime
import sqlalchemy as sa

from app.utilities.enums import TicketStatus

class Ticket(AuditTrailMixin, Base):
    __tablename__="ticket"

    ticket_id : Mapped[UUID] = mapped_column(sa.UUID, default=uuid4, index=True, primary_key=True)
    organization_id: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("organization.organization_id"), nullable=False)
    employee_id: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=False)
    asset_type_id: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("asset_type.asset_type_id"), nullable=False)
    ticket_title: Mapped[str] = mapped_column(String(255), nullable=False)
    ticket_description: Mapped[str] = mapped_column(String(1000), nullable=True)
    ticket_status: Mapped[str] = mapped_column(
        SQLAlchemyEnum(TicketStatus), 
        nullable=False, 
        default=TicketStatus.TODO
    )
    updated_by: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=True)

    organization = relationship("Organization", back_populates="tickets")
    employee = relationship("User", back_populates="tickets", foreign_keys=[employee_id])
    asset_type = relationship("AssetType", back_populates="tickets")

