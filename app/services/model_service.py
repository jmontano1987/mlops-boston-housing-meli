import os
import joblib
import mlflow
import mlflow.pyfunc
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

MODEL_SOURCE = os.getenv("MODEL_SOURCE", "none")
MLFLOW_URI = os.getenv("MLFLOW_URI", "file:./mlruns")


class ModelService:

    def __init__(self):
        try:
            if MODEL_SOURCE == "mlflow_remote":
                print("Modelo cargado desde MLflow REMOTO")
                mlflow.set_tracking_uri(MLFLOW_URI)
                self.model = mlflow.pyfunc.load_model("models:/boston_housing_rf@stage")

            elif MODEL_SOURCE == "mlflow_local":
                print("Modelo cargado desde MLflow LOCAL")
                mlflow.set_tracking_uri("file:./mlruns")
                self.model = mlflow.pyfunc.load_model("models:/boston_housing_rf@stage")

            elif MODEL_SOURCE == "none":
                print("CI mode: modelo no cargado")
                self.model = None

            else:
                print("Modelo cargado desde archivo LOCAL (model.pkl)")
                self.model = joblib.load("models/model.pkl")

        except Exception as e:
            print(f"Error cargando modelo: {e}")
            self.model = None

    def predict(self, data: dict) -> float:
        #features = np.array(list(data.values())).reshape(1, -1)
        if self.model is None:
            raise ValueError("Modelo no disponible")
        features = pd.DataFrame([data]) 
        prediction = self.model.predict(features)
        return float(prediction[0])


model_service = ModelService()