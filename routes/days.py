from models.days import Day, CreateUpdateDayRequest, UpdateDayRequest
from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from di.injection import db_dependency
from models.effects import Effect
from utils.constants import date_regex_pattern

router = APIRouter(prefix="/days", tags=["Day Routes"])


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_day(day: CreateUpdateDayRequest, db: db_dependency):
    new_day = Day(**day.model_dump())
    existing_day = db.query(Day).filter(Day.date == new_day.date).first()
    if existing_day:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Day already exists!")
    db.add(new_day)
    db.commit()


@router.get("/date", status_code=status.HTTP_200_OK)
async def get_day_by_date(db: db_dependency, date: str = Query(regex=date_regex_pattern)):
    day = db.query(Day).filter(Day.date == date).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day with the provided date is not found!")
    return day


@router.get("/id/{day_id}", status_code=status.HTTP_200_OK)
async def get_day_by_id(db: db_dependency, day_id: int = Path(gt=0)):
    day = db.query(Day).filter(Day.id == day_id).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day does not exist")
    return day


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_days(db: db_dependency):
    return db.query(Day).all()


@router.put("/id/{day_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_day(db: db_dependency, updated_day: UpdateDayRequest, day_id: int = Path(gt=0)):
    day = db.query(Day).filter(Day.id == day_id).first()
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
async def delete_day_by_id(db: db_dependency, day_id: int = Path(gt=0)):
    day = db.query(Day).filter(Day.id == day_id).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    db.query(Day).filter(Day.id == day_id).delete()
    db.query(Effect).filter(Effect.foreign_key == day_id).delete(synchronize_session=False)
    db.commit()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_days(db: db_dependency):
    db.query(Day).delete(synchronize_session=False)
    db.query(Effect).delete(synchronize_session=False)
    db.commit()
