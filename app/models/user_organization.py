from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from app.utilities.audit_trail_mixin import AuditTrailMixin
from app.utilities.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func


class UserOrganization(AuditTrailMixin, Base):
    __tablename__ = "user_organization"

    user_organization_id : Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4)
    user_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=False)
    organization_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("organization.organization_id"), nullable=False)

    user = relationship("User", back_populates="user_organizations")
    organization = relationship("Organization", back_populates="user_organizations")
