from typing import Optional
from sqlmodel import SQLModel, Field, ForeignKey


class Effect(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    time: str = Field(default=None)
    rate: int = Field(gt=-1, lt=5)
    description: str = Field(min_length=5, max_length=100)
    foreign_key: int = Field(ForeignKey("day.id"))

