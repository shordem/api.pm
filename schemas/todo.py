from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

from schemas.user import UserSchema


class TodoBase(BaseModel):
    title: str
    description: str
    due_date: str
    completed: bool
    folder_id: UUID4
    created_by: UUID4


class TodoCreate(BaseModel):
    title: str
    description: str
    due_date: datetime


class TodoSchema(BaseModel):
    id: UUID4
    title: str
    description: str
    due_date: datetime
    completed: bool
    created_by: UserSchema

    class Config:
        from_attributes = True


class TodoUpdate(TodoCreate):
    completed: bool
