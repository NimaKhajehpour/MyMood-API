from typing import Optional
from pydantic import BaseModel, Field as pyField
from sqlmodel import Field, SQLModel, ForeignKey
from models.effects import Effect

from utils.constants import date_regex_pattern


class Day(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    date: str = Field(default=None)
    red: int
    green: int
    blue: int
    rate: int
    auto_rate: bool
    owner: int = Field(ForeignKey("user.id"))


class UpdateDayRequest(BaseModel):
    red: Optional[int] = pyField(gt=-1, lt=256)
    green: Optional[int] = pyField(gt=-1, lt=256)
    blue: Optional[int] = pyField(gt=-1, lt=256)
    rate: Optional[int] = pyField(gt=-1, lt=5)
    auto_rate: Optional[bool] = pyField(default=False)


class CreateDayRequest(BaseModel):
    date: str = pyField(pattern=date_regex_pattern)
    red: int = pyField(gt=-1, lt=256)
    green: int = pyField(gt=-1, lt=256)
    blue: int = pyField(gt=-1, lt=256)
    rate: int = pyField(gt=-1, lt=5)
    auto_rate: bool = pyField(default=False)


class DaysEffectsModel(BaseModel):
    day: Day
    effects: list[Effect]


class DaysOverviewModel(BaseModel):
    data: list[DaysEffectsModel]
