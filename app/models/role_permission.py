from datetime import datetime
from uuid import UUID, uuid4
import sqlalchemy as sa

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities import AuditTrailMixin, Base

class RolePermission(AuditTrailMixin, Base):
    __tablename__ = "role_permission"

    role_permission_id : Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, index=True, default=uuid4)
    role_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("roles.role_id"), nullable=False)
    permission_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("permissions.permission_id"), nullable=False)

    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")