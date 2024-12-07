import hashlib
import hmac
from dotenv import load_dotenv
import os
import requests
from typing import Union

load_dotenv()
API_SECRET = os.getenv("API_KEY")
SHARED_SECRET = os.getenv("API_SHARED_SECRET")
API_URL = os.getenv("API_URL")


class ClimateApi:
    def __get_sig(self, query: str):
        return hmac.new(SHARED_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    
    def __get_query(self, lat, lon, expire_dt=1924948800):
        return f"/packages/basic-1h?lat={lat}&lon={lon}&apikey={API_SECRET}&expire={expire_dt}"

    def forecast_climate(self, lat: Union[str|int | float], lon:Union[str|int | float]):
        query = self.__get_query(lat, lon)
        sig = self.__get_sig(query)
        signed_url = f"https://my.meteoblue.com{query}&sig={sig}"
        try:
            response = requests.get(signed_url)
            response.raise_for_status()
            data = response.json()
        except:
            print(f"Erro ao obter a previsão climática: {e}")
            data = None 
        return data

