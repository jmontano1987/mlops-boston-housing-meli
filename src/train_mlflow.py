import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import pandas as pd

os.makedirs("models", exist_ok=True)

def train_model(X_train, y_train):
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(
            n_estimators=100,
            min_samples_leaf=4,
            max_features='sqrt',
            random_state=42
        ))
    ], memory=None)

    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    return rmse, r2


def save_model(model, path):
    joblib.dump(model, path)


def main():
    print("Configurando experimento MLflow...")
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("boston_housing")

    with mlflow.start_run():
        print("Preprocesando datos...")
        df = pd.read_csv("data/processed/data_clean.csv")

        X = df.drop(columns=["MEDV"])
        y = df["MEDV"]

        print("Dividiendo datos...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print("Entrenando modelo...")
        model = train_model(X_train, y_train)

        print("Evaluando modelo...")
        rmse, r2 = evaluate_model(model, X_test, y_test)

        print(f"RMSE: {rmse:.4f}")
        print(f"R2: {r2:.4f}")

        print("Registrando en MLflow...")
        mlflow.log_param("model", "RandomForest")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.sklearn.log_model(model, "model")
        run_id = mlflow.active_run().info.run_id
        print(f"Modelo registrado con run_id: {run_id}")
        mlflow.register_model(f"runs:/{run_id}/model", "boston_housing_rf")

        print("Guardando modelo local...")
        save_model(model, "models/model.pkl")

        print("Entrenamiento completo")


if __name__ == "__main__":
    main()
