from sqlmodel import SQLModel, Field, ForeignKey
from pydantic import BaseModel, Field as pyField


class Bug(SQLModel, table=True):
    id: int = Field(default=None, index=True, primary_key=True)
    username: str
    user_id: int = Field(ForeignKey("user.id"))
    description: str
    title: str
    approved: bool = Field(default=False)
    done: bool = Field(default=False)
    issue_link: str | None = Field(default=None)


class BugRequest(BaseModel):
    description: str = pyField(min_length=50, max_length=300)
    title: str = pyField(min_length=5, max_length=30)