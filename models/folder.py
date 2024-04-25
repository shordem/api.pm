from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.note import Note
from models.todo import Todo


class Folder(BaseModel):
    name = Column(String)
    organization_id = Column(UUID, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="folders")
    notes = relationship(Note, back_populates="folder")
    todos = relationship(Todo, back_populates="folder")
