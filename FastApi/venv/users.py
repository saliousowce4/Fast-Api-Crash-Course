from fastapi import FastAPI

from sqlalchemy import MetaData

app = FastAPI()

app.get("/")