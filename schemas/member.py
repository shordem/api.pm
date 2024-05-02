from pydantic import BaseModel


class MemberCreate(BaseModel):
    email: str


class UpdateMemberRole(BaseModel):
    role: str
