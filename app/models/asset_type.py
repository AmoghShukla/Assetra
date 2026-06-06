from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities import AuditTrailMixin
from app.utilities.base import Base
import sqlalchemy as sa

class AssetType(AuditTrailMixin, Base):
    __tablename__="asset_type"

    asset_type_id : Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, index=True, default=uuid4)
    asset_name : Mapped[str] = mapped_column(String(255), nullable=False)
    organization_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey('organization.organization_id'), nullable=False)
    
    organization = relationship("Organization", back_populates="asset_types")
    assets = relationship("Asset", back_populates="asset_type")
    tickets = relationship("Ticket", back_populates="asset_type")