from pydantic import BaseModel


class OrganizationBase(BaseModel):
    name: str
    image_url: str
    description: str
    owner_id: str


class OrganizationCreate(BaseModel):
    name: str
    owner_id: str


class OrganizationCreatePayload(BaseModel):
    name: str


class Organization(OrganizationBase):
    id: str

    class Config:
        from_attributes = True


class OrganizationUpdate(OrganizationBase):
    pass
