import pandas as pd
import os

# Ruta del archivo de datos raw
RUTA_ARCHIVO = "data/raw/movies.csv"


def cargar_datos(ruta):
    try:
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró el archivo en: {ruta}")

        df = pd.read_csv(ruta)
        print("✅ Datos cargados correctamente")
        print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
        return df

    except Exception as e:
        print(f"❌ Error en la ingesta: {e}")
        return None


if __name__ == "__main__":
    cargar_datos(RUTA_ARCHIVO)
