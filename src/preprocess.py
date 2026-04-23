# Importar librerías necesarias
import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw/HousingData.csv"
PROCESSED_PATH = "data/processed/data_clean.csv"

FEATURE_COLS = [
    "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM",
    "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT",
]
TARGET_COL = "MEDV"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Registros cargados: {len(df)}")
    return df

def save_data(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Datos guardados en: {path}")

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed > 0:
        print(f"Duplicados eliminados: {removed}")
    return df


def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum()
    cols_with_missing = missing[missing > 0].index.tolist()
    for col in cols_with_missing:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"Columna '{col}': {int(missing[col])} nulos imputados con mediana ({median_val:.4f})")
    return df


def remove_outliers(df: pd.DataFrame, col: str, lower_q: float = 0.01, upper_q: float = 0.99) -> pd.DataFrame:
    lower = df[col].quantile(lower_q)
    upper = df[col].quantile(upper_q)
    before = len(df)
    df = df[(df[col] >= lower) & (df[col] <= upper)]
    removed = before - len(df)
    if removed > 0:
        print(f"Outliers eliminados en '{col}': {removed} registros")
    return df

def split_features_target(df: pd.DataFrame, feature_cols: list, target_col: str) -> tuple:
    X = df[feature_cols]
    y = df[target_col]
    return X, y

def preprocess(path: str) -> tuple:
    df = load_data(path)
    df = remove_duplicates(df)
    df = impute_missing(df)
    df = remove_outliers(df, TARGET_COL) # En Random Forest no es tan crítico eliminar outliers, pero lo hacemos para mejorar la calidad de los datos

    print(f"Registros finales: {len(df)}")

    return split_features_target(df, FEATURE_COLS, TARGET_COL)


if __name__ == "__main__":
    df = load_data(RAW_PATH)
    df = remove_duplicates(df)
    df = impute_missing(df)
    df = remove_outliers(df, TARGET_COL)

    print(f"Registros finales: {len(df)}")

    save_data(df, PROCESSED_PATH)

    X, y = split_features_target(df, FEATURE_COLS, TARGET_COL)

    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
