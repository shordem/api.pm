from typing import Dict
from pydantic import BaseModel, Field


class EmailSchema(BaseModel):
    to: str
    subject: str
    template: str
    variables: Dict[str, str] = Field(...)
