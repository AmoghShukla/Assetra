from uuid import UUID, uuid4
import sqlalchemy as sa
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities import Base, AuditTrailMixin

class User(AuditTrailMixin, Base):
    __tablename__ = "user"

    user_id : Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4, index=True)
    user_name : Mapped[str] = mapped_column(String(255), nullable=False)
    user_email : Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    user_password : Mapped[str] = mapped_column(String(255), nullable=False)

    user_organizations = relationship("UserOrganization", back_populates="user")
    user_roles = relationship("UserRole", back_populates="user")
    user_permissions = relationship("UserPermission", back_populates="user", foreign_keys="[UserPermission.user_id]")
    tickets = relationship("Ticket", back_populates="employee", foreign_keys="Ticket.employee_id")
    asset_assignments = relationship("AssetAssignment", back_populates="assigned_to_user", foreign_keys="AssetAssignment.assigned_to")
