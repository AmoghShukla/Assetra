from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities.audit_trail_mixin import AuditTrailMixin
from app.utilities.base import Base

class AssetAssignment(AuditTrailMixin, Base):
    __tablename__ = "asset_assignment"

    asset_assignment_id : Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, index=True, default=uuid4)
    asset_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("asset.asset_id"), nullable=False)
    assigned_to : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=False)
    assigned_by : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=False)

    asset = relationship("Asset", back_populates="assignments")
    assigned_to_user = relationship("User", back_populates="asset_assignments", foreign_keys=[assigned_to])
