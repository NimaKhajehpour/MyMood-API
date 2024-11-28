from typing import List

from fastapi import APIRouter, Query, Path
from starlette import status
from models.effects import effects

router = APIRouter(prefix="/effects")


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_effects():
    return effects


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_effect(effect: dict):
    effects.append(effect)


@router.get("/foreign_key/{foreign_key}", status_code=status.HTTP_200_OK)
async def get_effects_by_day(foreign_key=int):
    effects_to_return = []
    for effect in effects:
        if effect.get("foreign-key") == int(foreign_key):
            effects_to_return.append(effect)
    return effects_to_return


@router.get("/filter")
async def query_effects(rate: List[int] = Query()):
    effects_to_return = []
    for effect in effects:
        if effect.get("rate") in rate:
            effects_to_return.append(effect)

    return effects_to_return


@router.put("/id/{effect_id}")
async def update_effect(updated_effect: dict, effect_id:int = Path()):
    for effect in effects:
        if effect.get("id") == effect_id:
            effect.update(updated_effect)


@router.get("/id/{id}")
async def get_effect_by_id(id: int):
    for effect in effects:
        if effect.get("id") == int(id):
            return effect


@router.delete("/id/{id}")
async def delete_effect(id: int):
    for index, effect in enumerate(effects):
        if effect.get("id") == int(id):
            effects.pop(index)


@router.delete("/foreign_key/{foreign_key}")
async def delete_day_effects(foreign_key: int):
    effects_to_remove = []
    for index, effect in enumerate(effects):
        if effect.get("foreign-key") == int(foreign_key):
            effects_to_remove.append(index)
    effects_to_remove.sort(reverse=True)

    if effects_to_remove:
        for index in effects_to_remove:
            effects.pop(index)


@router.delete("")
async def delete_all_effects():
    effects.clear()