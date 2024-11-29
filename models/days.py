from typing import Optional
from sqlmodel import Field, SQLModel


class Day(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    date: str = Field(default=None, unique=True)
    red: int = Field(gt=-1, lt=256)
    green: int = Field(gt=-1, lt=256)
    blue: int = Field(gt=-1, lt=256)
    rate: int = Field(gt=-1, lt=5)
    auto_rate: bool = Field(default=False)