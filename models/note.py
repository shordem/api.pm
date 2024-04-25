from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Note(BaseModel):
    title = Column(String)
    content = Column(String)
    folder_id = Column(UUID, ForeignKey("folders.id"))
    created_by = Column(UUID, ForeignKey("users.id"))

    folder = relationship("Folder", back_populates="notes")
    creator = relationship("User", back_populates="notes")
