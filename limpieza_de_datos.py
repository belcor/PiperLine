#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# Rutas predeterminadas
RUTA_ENTRADA = Path("data/raw/movies.csv")
RUTA_SALIDA = Path("data/processed/movies_clean.csv")


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    print("🔍 Iniciando limpieza de datos...")

    df = df.drop_duplicates()
    df = df.dropna(subset=["title", "year", "rating"])
    df["genre"] = df["genre"].fillna("Desconocido")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["year", "rating"])
    df["title"] = df["title"].astype(str).str.strip().str.title()
    df["genre"] = df["genre"].astype(str).str.strip().str.title()

    print("✅ Limpieza completada")
    return df


def main(ruta_entrada: Path = RUTA_ENTRADA, ruta_salida: Path = RUTA_SALIDA):
    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ruta_entrada}")

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(ruta_entrada)
    df_limpio = limpiar_datos(df)
    df_limpio.to_csv(ruta_salida, index=False)
    print(f"💾 Datos limpios guardados en: {ruta_salida}")


if __name__ == "__main__":
    main()
