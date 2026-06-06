from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import Enum as SQLAlchemyEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utilities import AuditTrailMixin, Base, RoleName


class Role(AuditTrailMixin, Base):
    __tablename__ = "roles"

    role_id : Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4, index=True)
    role_name : Mapped[str] = mapped_column(SQLAlchemyEnum(RoleName), nullable=False, unique=True)

    user_roles = relationship("UserRole", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role")