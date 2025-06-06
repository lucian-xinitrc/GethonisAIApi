from fastapi import FastAPI
from api import router
#Working
app = FastAPI()

app.include_router(router)