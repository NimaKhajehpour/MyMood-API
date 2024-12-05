from typing import Annotated

from models.days import Day, CreateDayRequest, UpdateDayRequest
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from di.injection import db_dependency
from models.effects import Effect
from utils.auth_utils import get_current_user
from utils.constants import date_regex_pattern

router = APIRouter(prefix="/days", tags=["Day Routes"])
user_dependency = Annotated[dict, Depends(get_current_user)]


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
    return db.query(Day).filter(Day.owner == user.get('id')).all()


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


@router.delete("/id/{day_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_day_by_id(user: user_dependency, db: db_dependency, day_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    day = db.query(Day).filter(Day.owner == user.get('id')).filter(Day.id == day_id).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    db.query(Day).filter(Day.owner == user.get('id')).filter(Day.id == day_id).delete()
    db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.foreign_key == day_id).delete(synchronize_session=False)
    db.commit()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_days(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    db.query(Day).filter(Day.owner == user.get('id')).delete(synchronize_session=False)
    db.query(Effect).filter(Effect.owner == user.get('id')).delete(synchronize_session=False)
    db.commit()
