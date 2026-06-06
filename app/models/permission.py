from uuid import UUID, uuid4
import sqlalchemy as sa
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utilities import  AuditTrailMixin, Base


class Permission(AuditTrailMixin, Base):
    __tablename__ = "permissions"

    permission_id :  Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4, index=True)
    permission_name : Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    permisssion_description : Mapped[str] = mapped_column(String(255), nullable=True)
    
    role_permissions = relationship("RolePermission", back_populates="permission")
    user_permissions = relationship("UserPermission", back_populates="permission")
