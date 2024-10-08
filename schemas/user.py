from pydantic import BaseModel, UUID4


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: UUID4

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserUpdate(UserBase):
    password: str
    is_email_verified: bool
