from typing import List, Annotated
from fastapi import APIRouter, Query, Path, HTTPException, Depends
from starlette import status

from models.days import Day
from models.effects import Effect, CreateEffectRequest, UpdateEffectRequest
from di.injection import db_dependency
from utils.auth_utils import get_current_user
from sqlmodel import func

router = APIRouter(prefix="/effects", tags=["Effect Routes"])
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_effects(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(Effect).filter(Effect.owner == user.get('id')).all()


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_effect(user: user_dependency, db: db_dependency, effect: CreateEffectRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    day = db.query(Day).filter(Day.id == effect.foreign_key).filter(Day.owner == user.get('id')).first()
    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day with given id not found")
    new_effect = Effect(**effect.model_dump(exclude={"owner"}), owner=user.get('id'))
    db.add(new_effect)
    db.commit()


@router.get("/avg", status_code=status.HTTP_200_OK)
async def get_day_avg(user: user_dependency, db: db_dependency, foreign_key: int = Query(gt=0)):
    sum, count = db.query(func.sum(Effect.rate).label("sum"), func.count(Effect.id).label("count")).filter(Effect.owner == user.get('id'))\
        .filter(Effect.foreign_key == foreign_key).one()
    day_avg = sum/count
    return day_avg


@router.get("/foreign_key/{foreign_key}", status_code=status.HTTP_200_OK)
async def get_effects_by_day(user: user_dependency, db: db_dependency, foreign_key: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.foreign_key == foreign_key).all()


@router.post("/filter", status_code=status.HTTP_200_OK)
async def query_effects(user: user_dependency, db: db_dependency, rate: List[int]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.rate.in_(rate)).all()


@router.put("/id/{effect_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_effect(user: user_dependency, db: db_dependency, updated_effect: UpdateEffectRequest, effect_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    effect = db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.id == effect_id).first()
    if not effect:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="effect not found")
    effect.time = updated_effect.time
    effect.rate = updated_effect.rate
    effect.description = updated_effect.description
    db.add(effect)
    db.commit()


@router.get("/id/{effect_id}", status_code=status.HTTP_200_OK)
async def get_effect_by_id(user: user_dependency, db: db_dependency, effect_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    effect = db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.id == effect_id).first()
    if not effect:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="effect not found")
    return effect


@router.delete("/id/{effect_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_effect(user: user_dependency, db: db_dependency, effect_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    effect_exists = db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.id == effect_id).first()
    if not effect_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.id == effect_id).delete()
    db.commit()


@router.delete("/foreign_key/{foreign_key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_day_effects(user: user_dependency, db: db_dependency, foreign_key: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    db.query(Effect).filter(Effect.owner == user.get('id')).filter(Effect.foreign_key == foreign_key).delete(synchronize_session=False)
    db.commit()


@router.delete("")
async def delete_all_effects(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    db.query(Effect).filter(Effect.owner == user.get('id')).delete(synchronize_session=False)
