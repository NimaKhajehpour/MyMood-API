from fastapi import FastAPI
from routes.effects import router as effects_router

app = FastAPI()

app.include_router(effects_router)



