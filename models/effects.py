from typing import Optional

from sqlmodel import SQLModel, Field, ForeignKey
from pydantic import BaseModel, Field as pyField

from utils.constants import time_regex_pattern


class Effect(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    time: str
    rate: int
    description: str
    foreign_key: int = Field(ForeignKey("day.id"))
    owner: int = Field(ForeignKey("user.id"))


class CreateEffectRequest(BaseModel):
    time: str = pyField(default=None, pattern=time_regex_pattern)
    rate: int = pyField(gt=-1, lt=5)
    description: str = pyField(min_length=5, max_length=100)
    foreign_key: int = pyField(gt=0)


class UpdateEffectRequest(BaseModel):
    time: Optional[str] = pyField(default=None, pattern=time_regex_pattern)
    rate: Optional[int] = pyField(gt=-1, lt=5)
    description: Optional[str] = pyField(min_length=5, max_length=100)