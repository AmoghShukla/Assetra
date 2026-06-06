from uuid import UUID,uuid4

import sqlalchemy as sa
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities import Base, AuditTrailMixin


class Organization(AuditTrailMixin, Base):
    __tablename__ = "organization"

    organization_id : Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4, index=True)
    organization_name : Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    user_organizations = relationship("UserOrganization", back_populates="organization")
    assets = relationship("Asset", back_populates="organization")
    tickets = relationship("Ticket", back_populates="organization")
    asset_types = relationship("AssetType", back_populates="organization")