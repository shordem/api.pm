from pydantic import BaseModel, UUID4

from schemas.folder import FolderSchema
from schemas.user import UserSchema


class TodoBase(BaseModel):
    title: str
    description: str
    due_date: str
    completed: bool
    folder_id: UUID4
    created_by: UUID4


class TodoCreate(TodoBase):
    pass


class TodoSchema:
    id: UUID4
    title: str
    description: str
    due_date: str
    completed: bool
    folder: FolderSchema
    created_by: UserSchema

    class Config:
        from_attributes = True


class TodoUpdate(TodoBase):
    id: UUID4
