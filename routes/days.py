from models.days import days
from fastapi import APIRouter, Path, Query
from starlette import status
from routes.effects import delete_day_effects, delete_all_effects

router = APIRouter(prefix="/days", tags=["Day Routes"])


@router.post("/new")
async def create_day(day: dict):
    days.append(day)


@router.get("/date")
async def get_day_by_date(date: str = Query()):
    for day in days:
        if day.get("date").casefold() == str(date.casefold()):
            return day


@router.get("/id/{id}")
async def get_day_by_id(id: int):
    for day in days:
        if day.get("id") == int(id):
            return day


@router.get("")
async def get_all_days():
    return days


@router.put("/id/{day_id}")
async def update_day(updated_day: dict, day_id: int):
    for day in days:
        if day.get("id") == int(day_id):
            day.update(updated_day)


@router.delete("/id/{id}")
async def delete_day_by_id(id: int):
    for index, day in enumerate(days):
        if day.get("id") == int(id):
            days.pop(index)
            await delete_day_effects(id)


@router.delete("")
async def delete_all_days():
    days.clear()
    await delete_all_effects()