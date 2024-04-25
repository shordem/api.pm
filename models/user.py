from sqlalchemy import Column, String, Boolean

from models.base import BaseModel

class User(BaseModel):
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    is_email_verified = Column(Boolean, default=False)
    password = Column(String)