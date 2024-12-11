from fastapi import APIRouter, HTTPException, Body
from models.User import User, UpdateUserPasswordRequest
from di.user_dependency import user_dependency
from di.injection import db_dependency
from utils.pass_crypt import bcrypt_context
from starlette import status
from models.days import Day
from models.effects import Effect
from models.bugs import Bug
from models.suggestions import Suggestion


router = APIRouter(
    prefix="/account",
    tags=['Account']
)


@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(db: db_dependency, user: user_dependency, password: UpdateUserPasswordRequest = Body()):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    requested_user = db.query(User).filter(User.id == user.get('id')).one()
    if not bcrypt_context.verify(password.current_password, requested_user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Password is not correct')
    if password.new_password != password.confirm_password:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='confirm password does not match')
    requested_user.password = bcrypt_context.hash(password.confirm_password)
    db.add(requested_user)
    db.commit()


@router.delete("/data", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account_data(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    db.query(Day).filter(Day.owner == user.get('id')).delete()
    db.query(Effect).filter(Effect.owner == user.get('id')).delete()
    db.query(Bug).filter(Bug.user_id == user.get('id')).delete()
    db.query(Suggestion).filter(Suggestion.user_id == user.get('id')).delete()
    db.commit() 