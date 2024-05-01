from sqlalchemy import Column, String

from models.base import BaseModel


class Permission(BaseModel):
    name = Column(String)
