from pydantic import BaseModel


class FolderBase(BaseModel):
    name: str
    organization_id: str


class FolderCreate(FolderBase):
    pass


class Folder(FolderBase):
    id: str

    class Config:
        from_attributes = True


class FolderUpdate(FolderBase):
    pass
