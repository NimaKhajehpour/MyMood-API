from sqlmodel import create_engine, SQLModel, Session
from utils.constants import database_url


engine = create_engine(database_url)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()