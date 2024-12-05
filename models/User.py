from sqlmodel import SQLModel, Field
from pydantic import BaseModel, Field as pyField


class User(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(unique=True, default=None)
    password: str


class UserRequest(BaseModel):
    username: str = pyField(min_length=3, max_length=16, pattern=r"^[a-zA-Z][a-zA-Z0-9_]{2,15}$")
    password: str = pyField(pattern=r"^[A-Za-z\d@$!%*?&]{8,}$", min_length=8)