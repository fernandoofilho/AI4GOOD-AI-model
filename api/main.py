from serializer import Serializer
from fastapi import FastAPI
from models import PayloadBody
from dependencies.climate_api import ClimateApi
from dependencies.model import Model 
from db import SessionLocal
from fastapi import Request

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


@app.get("/inferir2/")
def inferir(input_data: PayloadBody):
    data = model_ai.predict(input_data)
    return Serializer.serialize_many(data)  


@app.get("/api_climate/data")
async def get_climate_data(request: Request):
    input_data = await request.json()
    # try:
    lat = input_data["lat"]
    lon = input_data["lon"]
    data = climate_api.fetch_forecast(lat, lon)
    await climate_api.save_forecast_to_db(data, lat, lon)
    # except Exception as e:
    #     data = {"erro": f"Error during fetch data: {e}"}
    return Serializer.serialize_many(data)