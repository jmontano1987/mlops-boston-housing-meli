# Importar librerías
import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Crear carpeta models si no existe en el repo
os.makedirs("models", exist_ok=True)

# Cargar los datos
def load_data(path):
    return pd.read_csv(path)

# Dividir los datos en entrenamiento y prueba (80/20) y sacar la variable objetivo
def split_data(df):
    X = df.drop("MEDV", axis=1)
    y = df["MEDV"]
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un modelo de Random Forest
def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


# Evaluar el modelo con RMSE y R2
def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    
    return rmse, r2

# Guardar el modelo entrenado con joblib en la carpeta models
def save_model(model, path):
    joblib.dump(model, path)


def main():
    print("Cargar datos...")
    df = load_data("data/raw/HousingData.csv")

    print("Dividir datos...")
    X_train, X_test, y_train, y_test = split_data(df)

    print("Entrenar modelo...")
    model = train_model(X_train, y_train)

    print("Evaluar modelo...")
    rmse, r2 = evaluate_model(model, X_test, y_test)

    print(f"RMSE: {rmse}")
    print(f"R2: {r2}")

    print("Guardar modelo...")
    save_model(model, "models/model.pkl")

    print("Entrenamiento completo")

if __name__ == "__main__":
    main()