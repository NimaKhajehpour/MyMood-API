from typing import List
from fastapi import APIRouter, Query, Path, HTTPException
from starlette import status
from models.effects import Effect
from di.injection import db_dependency
from sqlmodel import func

router = APIRouter(prefix="/effects", tags=["Effect Routes"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_effects(db: db_dependency):
    return db.query(Effect).all()


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_effect(db: db_dependency, effect: Effect):
    new_effect = Effect(**effect.model_dump(exclude={"id"}))
    db.add(new_effect)
    db.commit()


@router.get("/avg", status_code=status.HTTP_200_OK)
async def get_day_avg(db: db_dependency, foreign_key: int = Query(gt=0)):
    sum, count = db.query(func.sum(Effect.rate).label("sum"), func.count(Effect.id).label("count")).filter(Effect.foreign_key == foreign_key).one()
    day_avg = sum/count
    return day_avg


@router.get("/foreign_key/{foreign_key}", status_code=status.HTTP_200_OK)
async def get_effects_by_day(db: db_dependency, foreign_key: int = Path(gt=0)):
    return db.query(Effect).filter(Effect.foreign_key == foreign_key).all()


@router.post("/filter", status_code=status.HTTP_200_OK)
async def query_effects(db: db_dependency, rate: List[int]):
    return db.query(Effect).filter(Effect.rate.in_(rate)).all()


@router.put("/id/{effect_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_effect(db: db_dependency, updated_effect: Effect, effect_id: int = Path(gt=0)):
    effect = db.query(Effect).filter(Effect.id == effect_id).first()
    if not effect:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="effect not found")
    effect.time = updated_effect.time
    effect.rate = updated_effect.rate
    effect.description = updated_effect.description
    db.add(effect)
    db.commit()


@router.get("/id/{effect_id}", status_code=status.HTTP_200_OK)
async def get_effect_by_id(db: db_dependency, effect_id: int = Path(gt=0)):
    effect = db.query(Effect).filter(Effect.id == effect_id).first()
    if not effect:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="effect not found")
    return effect


@router.delete("/id/{effect_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_effect(db: db_dependency, effect_id: int = Path(gt=0)):
    effect_exists = db.query(Effect).filter(Effect.id == effect_id).exists()
    if not effect_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(Effect).filter(Effect.id == effect_id).delete()
    db.commit()


@router.delete("/foreign_key/{foreign_key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_day_effects(db: db_dependency, foreign_key: int = Path(gt=0)):
    db.query(Effect).filter(Effect.foreign_key == foreign_key).delete(synchronize_session=False)
    db.commit()


@router.delete("")
async def delete_all_effects(db: db_dependency):
    db.query(Effect).delete(synchronize_session=False)
