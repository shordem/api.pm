from sqlalchemy import Column, String, ForeignKey, UUID, Boolean
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.note import Note
from models.todo import Todo


class Folder(BaseModel):
    name = Column(String)
    organization_id = Column(UUID, ForeignKey("organizations.id"))
    is_default = Column(Boolean, default=False)

    organization = relationship("Organization", back_populates="folders")
    notes = relationship(Note, back_populates="folder")
    todos = relationship(Todo, back_populates="folder")
