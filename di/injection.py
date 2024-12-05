from database.database import get_db
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from utils.constants import oauth2bearer

db_dependency = Annotated[Session, Depends(get_db)]

token_dependency = Annotated[str, Depends(oauth2bearer)]

form_data_injection = Annotated[OAuth2PasswordRequestForm, Depends()]