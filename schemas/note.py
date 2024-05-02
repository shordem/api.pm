from pydantic import BaseModel, UUID4

from schemas.folder import FolderSchema
from schemas.user import UserSchema


class NoteBase(BaseModel):
    title: str
    content: str
    folder_id: UUID4
    created_by: UUID4


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteSchema(BaseModel):
    id: UUID4
    title: str
    content: str
    created_by: UserSchema

    class Config:
        from_attributes = True


class NoteUpdate(NoteCreate):
    pass
