from sqlalchemy import Column, String

from models.base import BaseModel


class Role(BaseModel):
    name = Column(String)
