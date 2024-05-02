from sqlalchemy import Column, String, ForeignKey, UUID, Boolean
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.user import User


class Code(BaseModel):
    code = Column(String)
    user_id = Column(UUID, ForeignKey("users.id"))

    user = relationship(User, back_populates="codes")
