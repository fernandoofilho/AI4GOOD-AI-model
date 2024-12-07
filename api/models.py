from pydantic import BaseModel
from typing import Any
from sqlalchemy import Column, Integer, String, Float
from db import Base

class PayloadBody(BaseModel):
    data: Any


# class ApiForecats(Base):
#    __tablename__="Forecasts"
#    """forecats - adc dps"""