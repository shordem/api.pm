from pydantic import BaseModel


class MemberCreate(BaseModel):
    email: str
