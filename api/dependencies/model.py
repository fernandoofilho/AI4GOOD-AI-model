import pickle
import pandas as pd
import os
from dotenv import load_dotenv
from joblib import load

load_dotenv()
class Model:
    def __init__(self, model_path = os.getenv("MODEL_PATH")):
        self.model_path =  model_path 
        self.model = self.__load_model()

    
    def __load_model(self):
        try:
            model = load(self.model_path)
            if not hasattr(model, "predict"):
                raise Exception("Loaded object is not a valid model with a 'predict' method.")
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

        input_data["data_pas"] = pd.to_datetime(input_data["data_pas"])
        input_data["month"] = input_data["data_pas"].dt.month
        input_data["day_of_year"] = input_data["data_pas"].dt.dayofyear

        input_data = input_data.drop(columns=["data_pas"])

        expected_columns = ['lat', 'lon', 'numero_dias_sem_chuva', 'precipitacao', 'month', 'day_of_year']
        input_data = input_data[expected_columns]

        try:
            prediction = self.model.predict(input_data)
            return int(prediction[0])
        except Exception as e:
            raise Exception(f"Error during prediction: {e}")
