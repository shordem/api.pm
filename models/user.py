from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from models import base
from models.user_organization import UserOrganization


class User(base.BaseModel):
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    is_email_verified = Column(Boolean, default=False)
    password = Column(String)

    organizations = relationship(UserOrganization, back_populates="user")
    todos = relationship("Todo", back_populates="creator")
    notes = relationship("Note", back_populates="creator")
