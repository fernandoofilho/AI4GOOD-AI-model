import pickle
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
class Model:
    def __init__(self, model_path = os.getenv("MODEL_PATH")):
        self.model_path =  model_path 
        self.model = self.__load_model()

    def __load_model(self):
        try:
            with open(self.model_path, 'rb') as file:
                model = pickle.load(file)
            return model
        except FileNotFoundError:
            raise Exception(f"Model file not found at {self.model_path}")
        except Exception as e:
            raise Exception(f"{e}")

    def predict(self, lat, lon, data_pas, numero_dias_sem_chuva, precipitacao):
        input_data = pd.DataFrame({
            'lat': [lat],
            'lon': [lon],
            'data_pas': [data_pas],
            'numero_dias_sem_chuva': [numero_dias_sem_chuva],
            'precipitacao': [precipitacao]
        })
        try:
            prediction = self.model.predict(input_data)
            return int(prediction[0])
        except Exception as e:
            raise Exception(f"Error during prediction: {e}")
