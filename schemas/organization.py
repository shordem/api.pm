from pydantic import BaseModel, UUID4


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
    id: UUID4
    name: str
    image_url: str

    class Config:
        from_attributes = True


class OrganizationUpdate(OrganizationBase):
    pass
