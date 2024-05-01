from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Organization(BaseModel):
    name = Column(String)
    image_url = Column(String, nullable=True)
    description = Column(String, default="")
    owner_id = Column(UUID, ForeignKey("users.id"))

    folders = relationship(
        "Folder", back_populates="organization", cascade="all, delete-orphan"
    )
    user_organizations = relationship(
        "UserOrganization", back_populates="organization", cascade="all, delete-orphan"
    )
