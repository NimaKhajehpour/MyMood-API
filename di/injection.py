from database.database import get_db
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session


db_dependency = Annotated[Session, Depends(get_db)]