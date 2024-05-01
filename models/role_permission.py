from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models.base import BaseModel


class RolePermission(BaseModel):
    role_id = Column(UUID, ForeignKey("roles.id"))
    permission_id = Column(UUID, ForeignKey("permissions.id"))
