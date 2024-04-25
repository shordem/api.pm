from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, UUID
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Todo(BaseModel):
    title = Column(String)
    description = Column(String)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    folder_id = Column(UUID, ForeignKey("folders.id"))
    created_by = Column(UUID, ForeignKey("users.id"))

    folder = relationship("Folder", back_populates="todos")
    creator = relationship("User", back_populates="todos")
