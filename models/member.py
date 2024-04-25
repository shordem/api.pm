from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Member(BaseModel):
    organization_id = Column(UUID, ForeignKey("organizations.id"))
    user_id = Column(UUID, ForeignKey("users.id"))

    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="members")
