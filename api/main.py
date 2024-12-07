from serializer import Serializer
from fastapi import FastAPI
from models import PayloadBody
from dependencies.climate_api import ClimateApi
from dependencies.model import Model 
from db import SessionLocal

app = FastAPI()
model_ai = Model()
climate_api = ClimateApi()

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/")
def read_root():
    return {"root": "Hello AI4GOOD"}


@app.get("/inferir/")
def inferir(input_data: PayloadBody):
    data = model_ai.predict(input_data)
    return Serializer.serialize_data(data)


@app.get("/inferir/")
def inferir(input_data: PayloadBody):
    data = model_ai.predict(input_data)
    return Serializer.serialize_many(data)