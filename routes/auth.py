from fastapi import APIRouter, HTTPException
from datetime import timedelta
from starlette import status
from utils.auth_utils import authenticate_user, create_access_token
from utils.pass_crypt import bcrypt_context
from di.injection import db_dependency, form_data_injection
from models.User import UserRequest, User
from models.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(db: db_dependency, create_user: UserRequest):
    user = db.query(User).filter(User.username == create_user.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    user_model = User(
        username=create_user.username,
        password=bcrypt_context.hash(create_user.password),
    )

    db.add(user_model)
    db.commit()
    signed_up_user = authenticate_user(create_user.username, create_user.password, db)
    token = create_access_token(signed_up_user.username, signed_up_user.id, signed_up_user.role, timedelta(days=20))
    return {"access_token": token, 'token_type': 'Bearer'}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: form_data_injection, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    token = create_access_token(user.username, user.id, user.role, timedelta(days=20))
    return {'access_token': token, 'token_type': 'Bearer'}
