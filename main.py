from typing import Annotated

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session

from database.database import engine, get_db
from models.User import User
from routes.effects import router as effects_router
from routes.days import router as days_router
from routes.auth import router as auth_router
from routes.news import router as news_router
from routes.admin import admin_news_router, admin_bugs_router

import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def create_first_admin():
    db = next(get_db())
    admin = db.query(User).filter(User.role == 'admin').first()
    if not admin:
        first_admin_username = os.getenv("FIRST-ADMIN-USERNAME")
        first_admin_password = os.getenv("FIRST-ADMIN-PASSWORD")
        user_admin = User(username=first_admin_username, password=first_admin_password, role='admin')
        db.add(user_admin)
        db.commit()


app.include_router(effects_router)
app.include_router(days_router)
app.include_router(auth_router)
app.include_router(news_router)
app.include_router(admin_news_router)
app.include_router(admin_bugs_router)


# TODO: for running the app publicly in all the devices on the network do ipconfig
