from pydantic import BaseModel

from .user import UserSchema


class MemberCreate(BaseModel):
    email: str


class UpdateMemberRole(BaseModel):
    role: str


class ListMember(UserSchema):
    role: str
