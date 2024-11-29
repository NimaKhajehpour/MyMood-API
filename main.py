from fastapi import FastAPI
from sqlmodel import SQLModel

from database.database import engine
from routes.effects import router as effects_router
from routes.days import router as days_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(effects_router)
app.include_router(days_router)


# TODO: for running the app publicly in all the devices on the network do ipconfig
