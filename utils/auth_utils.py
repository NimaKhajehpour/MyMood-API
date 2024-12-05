from jose import jwt, JWTError
from starlette import status
from utils.pass_crypt import bcrypt_context
from di.injection import db_dependency, token_dependency
from models.User import User
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

def authenticate_user(username: str, password: str, db: db_dependency):
    requested_user: User = db.query(User).filter(User.username == username).first()
    if not requested_user:
        return False
    if not bcrypt_context.verify(password, requested_user.password):
        return False
    return requested_user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


async def get_current_user(token: token_dependency):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

