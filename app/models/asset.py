from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities import Base, AuditTrailMixin
import sqlalchemy as sa

from app.utilities.enums import AssetStatus

class Asset(AuditTrailMixin, Base):
    __tablename__="asset"

    asset_id : Mapped[UUID] = mapped_column(sa.UUID, default=uuid4, primary_key=True, index=True)
    asset_type_id : Mapped[UUID] = mapped_column(sa.UUID, ForeignKey('asset_type.asset_type_id'), nullable=False)
    organization_id: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("organization.organization_id"), nullable=False)
    asset_code : Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    asset_description : Mapped[str] = mapped_column(String(1000), nullable=True)
    asset_status: Mapped[AssetStatus] = mapped_column(
        SQLAlchemyEnum(AssetStatus), 
        nullable=False, 
        default=AssetStatus.AVAILABLE
    )
    updated_by: Mapped[UUID] = mapped_column(sa.UUID, ForeignKey("user.user_id"), nullable=True)

    asset_type = relationship("AssetType", back_populates="assets")
    organization = relationship("Organization", back_populates="assets")
    assignments = relationship("AssetAssignment", back_populates="asset")
