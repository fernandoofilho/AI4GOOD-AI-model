from pydantic import BaseModel
from typing import Any
from sqlalchemy import Column, Integer, String, Float
from db import Base

class PayloadBody(BaseModel):
    data: Any

class ApiForecastHeader(Base):
    __tablename__ = "ForecastsHeader"
    id = Column(Integer, primary_key=True, index=True)
    modelrun = Column(String, nullable=False)
    name = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    timezone_abbrevation = Column(String, nullable=True)
    latitude = Column(Integer, nullable=True)
    modelrun_utc = Column(String, nullable=True)
    longitude = Column(Integer, nullable=True)
    utc_timeoffset = Column(Integer, nullable=True)
    generation_time_ms = Column(Float, nullable=True)

class Units(Base):
    __tablename__ = "Units"

    id = Column(Integer, primary_key=True, index=True)
    modelrun = Column(String, nullable=False)
    precipitation = Column(String, nullable=True)
    windspeed = Column(String, nullable=True)
    precipitation_probability = Column(String, nullable=True)
    relativehumidity = Column(String, nullable=True)
    temperature = Column(String, nullable=True)
    time = Column(String, nullable=True)
    pressure = Column(String, nullable=True)
    winddirection = Column(String, nullable=True)

class ApiForecastItem(Base):
    __tablename__ = "Forecasts"
    id = Column(Integer, primary_key=True, index=True)
    modelrun = Column(String, nullable=False)

    date_forecast = Column(String, nullable=True)
    windspeed = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    precipitation_probability = Column(Float, nullable=True)
    convective_precipitation = Column(Float, nullable=True)
    rainspot = Column(String, nullable=True)
    pictocode = Column(Float, nullable=True)
    felttemperature = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    isdaylight = Column(Float, nullable=True)
    uvindex = Column(Float, nullable=True)
    relativehumidity = Column(Float, nullable=True)
    sealevelpressure = Column(Float, nullable=True)
    winddirection = Column(Float, nullable=True)
