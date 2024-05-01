from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.organization import Organization
from models.role import Role


class UserOrganization(BaseModel):
    organization_id = Column(UUID, ForeignKey("organizations.id"))
    user_id = Column(UUID, ForeignKey("users.id"))
    role_id = Column(UUID, ForeignKey("roles.id"))

    organization = relationship(Organization, back_populates="user_organizations")
    user = relationship("User", back_populates="organizations")
    role = relationship(Role)
