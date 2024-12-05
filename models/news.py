from sqlmodel import SQLModel, Field
from pydantic import BaseModel, Field as pyField


class News(SQLModel, table=True):
    id: int = Field(default=None, index=True, primary_key=True)
    title: str
    description: str


class NewsRequest(BaseModel):
    title: str = pyField(min_length=5, max_length=100)
    description: str = pyField(min_length=20, max_length=1000)