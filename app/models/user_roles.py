from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import  ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities.audit_trail_mixin import AuditTrailMixin
from app.utilities.base import Base


class UserRole(AuditTrailMixin, Base):
    __tablename__ = "user_role"

    user_role_id : Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4, index=True)
    user_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=False)
    role_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("roles.role_id"), nullable=False)
    

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")