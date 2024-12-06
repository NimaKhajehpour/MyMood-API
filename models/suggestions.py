from sqlmodel import SQLModel, Field, ForeignKey
from pydantic import BaseModel, Field as pyField


class Suggestion(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    username: str
    user_id: int = Field(ForeignKey("user.id"))
    description: str
    approved: bool = Field(default=False)
    done: bool = Field(default=False)
    issue_link: str | None = Field(default=None)


class SuggestionRequest(BaseModel):
    description: str = pyField(max_length=300, min_length=30)