from fastapi import FastAPI
from api import router

# Made by Lucian-Florin

app = FastAPI()

app.include_router(router)