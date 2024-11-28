from fastapi import FastAPI
from routes.effects import router as effects_router
from routes.days import router as days_router

app = FastAPI()

app.include_router(effects_router)
app.include_router(days_router)



