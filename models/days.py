from typing import Optional

from pydantic import BaseModel, Field as pyField
from sqlmodel import Field, SQLModel

from utils.constants import date_regex_pattern


class Day(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    date: str = Field(default=None, unique=True)
    red: int
    green: int
    blue: int
    rate: int
    auto_rate: bool


class UpdateDayRequest(BaseModel):
    red: Optional[int] = pyField(gt=-1, lt=256)
    green: Optional[int] = pyField(gt=-1, lt=256)
    blue: Optional[int] = pyField(gt=-1, lt=256)
    rate: Optional[int] = pyField(gt=-1, lt=5)
    auto_rate: Optional[bool] = pyField(default=False)


class CreateUpdateDayRequest(BaseModel):
    date: str = pyField(pattern=date_regex_pattern)
    red: int = pyField(gt=-1, lt=256)
    green: int = pyField(gt=-1, lt=256)
    blue: int = pyField(gt=-1, lt=256)
    rate: int = pyField(gt=-1, lt=5)
    auto_rate: bool = pyField(default=False)