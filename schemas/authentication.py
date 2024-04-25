from pydantic import BaseModel

class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    user_id: str | None = None

class LoginData(BaseModel):
    username: str
    password: str

class VerifyEmail(BaseModel):
    email: str