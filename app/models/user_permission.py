from datetime import datetime
from uuid import UUID, uuid4
import sqlalchemy as sa

from app.utilities.audit_trail_mixin import AuditTrailMixin
from app.utilities.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func, String


class UserPermission(AuditTrailMixin, Base):
    __tablename__ = "user_permission"

    user_permission_id: Mapped[UUID] = mapped_column(sa.UUID, default=uuid4, primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=False)
    permission_id: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("permissions.permission_id"), nullable=False)
    is_granted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    granted_by: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=True)
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_by: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=True)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    revoking_reason: Mapped[str] = mapped_column(String(500), nullable=True)

    user = relationship("User", back_populates="user_permissions", foreign_keys=[user_id])
    permission = relationship("Permission", back_populates="user_permissions")
