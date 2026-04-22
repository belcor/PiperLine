#!/usr/bin/env python3
import pandas as pd
from datetime import datetime
from pathlib import Path

RUTA_ENTRADA = Path("data/processed/movies_clean.csv")
RUTA_SALIDA = Path("data/processed/movies_validated.csv")
RUTA_REPORTE = Path("data/reports/validation_report.txt")

COLUMNAS_REQUERIDAS = ["title", "year", "rating", "genre", "director", "language"]
IDIOMAS_VALIDOS = ["English", "Korean", "Japanese", "French", "Portuguese", "Spanish"]
ANIO_MAXIMO = datetime.now().year
ANIO_MINIMO = 1900


def validar_estructura(df: pd.DataFrame) -> list:
    errores = []

    # Columnas obligatorias
    columnas_faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    if columnas_faltantes:
        errores.append(f"Columnas faltantes: {', '.join(columnas_faltantes)}")
        return errores

    # Clave primaria compuesta: title + year
    if df.duplicated(subset=["title", "year"]).any():
        dupes = df[df.duplicated(subset=["title", "year"], keep=False)][["title", "year"]]
        errores.append(
            f"Duplicados en clave primaria (title, year): {len(dupes)} registros duplicados"
        )

    return errores


def validar_semantica(df: pd.DataFrame) -> list:
    errores = []

    for idx, row in df.iterrows():
        if pd.isna(row["title"]) or str(row["title"]).strip() == "":
            errores.append(f"Fila {idx}: title vacío")

        try:
            year = int(row["year"])
            if year < ANIO_MINIMO or year > ANIO_MAXIMO:
                errores.append(f"Fila {idx}: year {year} fuera de rango ({ANIO_MINIMO}-{ANIO_MAXIMO})")
        except Exception:
            errores.append(f"Fila {idx}: year inválido ({row['year']})")

        try:
            rating = float(row["rating"])
            if rating < 0 or rating > 10:
                errores.append(f"Fila {idx}: rating {rating} fuera de rango (0-10)")
        except Exception:
            errores.append(f"Fila {idx}: rating inválido ({row['rating']})")

        if pd.isna(row["genre"]) or str(row["genre"]).strip() == "":
            errores.append(f"Fila {idx}: genre vacío")

        if pd.isna(row["director"]) or str(row["director"]).strip() == "":
            errores.append(f"Fila {idx}: director vacío")

        idioma = str(row["language"]).strip().title()
        if idioma not in IDIOMAS_VALIDOS:
            errores.append(f"Fila {idx}: language '{row['language']}' no está en la lista permitida")

    return errores


def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["title"] = df["title"].astype(str).str.strip().str.title()
    df["genre"] = df["genre"].astype(str).str.strip().str.title()
    df["director"] = df["director"].astype(str).str.strip()
    df["language"] = df["language"].astype(str).str.strip().str.title()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    def categoria_rating(value):
        if pd.isna(value):
            return "Desconocido"
        if value >= 8.0:
            return "Alto"
        if value >= 6.0:
            return "Medio"
        return "Bajo"

    df["rating_category"] = df["rating"].apply(categoria_rating)
    return df


def generar_reporte(errores: list, registros_evaluados: int, ruta_reporte: Path):
    ruta_reporte.parent.mkdir(parents=True, exist_ok=True)
    with ruta_reporte.open("w", encoding="utf-8") as reporte:
        reporte.write("VALIDACIÓN DE DATOS\n")
        reporte.write("====================\n")
        reporte.write(f"Fecha: {datetime.now().isoformat()}\n")
        reporte.write(f"Registros evaluados: {registros_evaluados}\n")
        reporte.write(f"Errores encontrados: {len(errores)}\n\n")

        if errores:
            reporte.write("DETALLE DE ERRORES:\n")
            for error in errores:
                reporte.write(f"- {error}\n")
        else:
            reporte.write("No se encontraron errores de validación.\n")

    print(f"📄 Reporte de validación generado en: {ruta_reporte}")


def main():
    if not RUTA_ENTRADA.exists():
        raise FileNotFoundError(f"No se encontró el dataset limpio en: {RUTA_ENTRADA}")

    print("🔎 Cargando dataset limpio para validación...")
    df = pd.read_csv(RUTA_ENTRADA)

    print("✅ Realizando validación estructural...")
    errores = validar_estructura(df)

    print("✅ Realizando validación semántica...")
    errores.extend(validar_semantica(df))

    df_transformado = transformar_datos(df)
    df_transformado.to_csv(RUTA_SALIDA, index=False)
    print(f"💾 Dataset validado guardado en: {RUTA_SALIDA}")

    generar_reporte(errores, len(df), RUTA_REPORTE)

    if errores:
        print(f"⚠️ Se encontraron {len(errores)} errores. Revisa {RUTA_REPORTE}")
    else:
        print("✅ Validación completada sin errores.")


if __name__ == "__main__":
    main()
