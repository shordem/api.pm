from pydantic import BaseModel, UUID4


class FolderBase(BaseModel):
    name: str
    organization_id: UUID4
    is_default: bool


class FolderCreate(BaseModel):
    name: str


class FolderSchema(FolderBase):
    id: UUID4

    class Config:
        from_attributes = True


class FolderUpdate(FolderBase):
    id: UUID4
