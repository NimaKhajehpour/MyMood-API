from typing import Annotated

from di.user_dependency import user_dependency
from models.days import Day, CreateDayRequest, UpdateDayRequest, DaysOverviewModel, DaysEffectsModel
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from di.injection import db_dependency
from models.effects import Effect
from utils.auth_utils import get_current_user
from utils.constants import date_regex_pattern
from sqlmodel import func, join, outerjoin

router = APIRouter(prefix="/days", tags=["Day Routes"])


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_day(day: CreateDayRequest, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    new_day = Day(**day.model_dump(exclude={"owner"}), owner=user.get('id'))
    existing_day = db.query(Day).filter(Day.owner == user.get('id')).filter(Day.date == new_day.date).first()
    if existing_day:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Day already exists!")
    db.add(new_day)
    db.commit()


@router.get("/date", status_code=status.HTTP_200_OK)
async def get_day_by_date(db: db_dependency, user: user_dependency, date: str = Query(regex=date_regex_pattern)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    day = db.query(Day).filter(Day.owner == user.get('id')).filter(Day.date == date).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day with the provided date is not found!")
    return day


@router.get("/id/{day_id}", status_code=status.HTTP_200_OK)
async def get_day_by_id(db: db_dependency, user: user_dependency, day_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    day = db.query(Day).filter(Day.owner == user.get('id')).filter(Day.id == day_id).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day does not exist")
    return day


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_days(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    query = (
        db.query(
            Day,
            (func.coalesce(func.sum(Effect.rate), 0) / func.coalesce(func.count(Effect.id), 1)).label("avg")
        )
        .outerjoin(Effect, Effect.foreign_key == Day.id)  # Use an outer join here
        .filter(Day.owner == user.get('id'))
        .group_by(Day.id)
        .all()
    )
    result = [
        {
            "day": day,
            "average": avg
        }
        for day, avg in query
    ]
    return result


@router.put("/id/{day_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_day(user: user_dependency, db: db_dependency, updated_day: UpdateDayRequest, day_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    day = db.query(Day).filter(Day.owner == user.get('id')).filter(Day.id == day_id).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    day.red = updated_day.red
    day.green = updated_day.green
    day.blue = updated_day.blue
    day.rate = updated_day.rate
    day.auto_rate = updated_day.auto_rate
    db.add(day)
    db.commit()


@router.get("/overview", status_code=status.HTTP_200_OK)
async def get_days_overview(db: db_dependency, user: user_dependency, days_id: list[int] = Query()):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    query = (
        db.query(Day, Effect)
        .outerjoin(Effect, Effect.foreign_key == Day.id)  # Outer join to include all days
        .filter(Day.owner == user.get("id"))
        .filter(Day.id.in_(days_id))
        .all()
    )

    # Group effects by day
    days_dict = {}
    for day, effect in query:
        if day.id not in days_dict:
            days_dict[day.id] = {
                "day": day,
                "effects": []
            }
        if effect:
            days_dict[day.id]["effects"].append(effect)

    day_overview = [
        DaysEffectsModel(day=data["day"], effects=data["effects"])
        for data in days_dict.values()
    ]

    return DaysOverviewModel(data=day_overview)


@router.delete("/id/{day_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_day_by_id(user: user_dependency, db: db_dependency, day_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    day = db.query(Day).filter(Day.owner == user.get('id')).filter(Day.id == day_id).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    db.query(Day).filter(Day.owner == user.get('id')).filter(Day.id == day_id).delete()
    db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.foreign_key == day_id).delete(
        synchronize_session=False)
    db.commit()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_days(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    db.query(Day).filter(Day.owner == user.get('id')).delete(synchronize_session=False)
    db.query(Effect).filter(Effect.owner == user.get('id')).delete(synchronize_session=False)
    db.commit()
