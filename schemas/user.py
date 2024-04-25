from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    is_email_verified: bool

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    password: str
    is_email_verified: bool
 