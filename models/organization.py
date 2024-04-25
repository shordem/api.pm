from sqlalchemy import Column, String, ForeignKey, UUID, orm
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Organization(BaseModel):
    name = Column(String)
    image_url = Column(String, nullable=True)
    description = Column(String, default="")
    owner_id = Column(UUID, ForeignKey("users.id"))

    owner = relationship("User", back_populates="organizations")
    folders = relationship(
        "Folder", back_populates="organization", cascade="all, delete-orphan"
    )
    members = relationship(
        "Member", back_populates="organization", cascade="all, delete-orphan"
    )
