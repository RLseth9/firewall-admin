from fastapi import FastAPI
from app.routes import machines

app = FastAPI()

app.include_router(machines.router)