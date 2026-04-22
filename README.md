# PiperLine

Proyecto de pipeline de datos para ingesta, limpieza y validación.

## Estructura

- `data/raw/` – datos originales sin procesar
- `data/processed/` – datos limpios y validados
- `data/reports/` – reportes de validación generados automáticamente
- `ingesta.py` – carga de datos desde `data/raw/`
- `limpieza_de_datos.py` – limpieza y normalización básica
- `validacion_datos.py` – validación estructural y semántica del dataset limpio

## Cómo ejecutar

1. Cargar el dataset:

```bash
python ingesta.py
```

2. Limpiar los datos:

```bash
python limpieza_de_datos.py
```

3. Validar el dataset limpio:

```bash
python validacion_datos.py
```

## Qué hace `validacion_datos.py`

- Verifica la presencia de columnas obligatorias
- Valida unicidad de clave primaria `title + year`
- Comprueba rangos y tipos de los campos `year` y `rating`
- Revisa valores permitidos en `language`
- Genera categoría `rating_category`
- Escribe el resultado validado en `data/processed/movies_validated.csv`
- Genera un reporte en `data/reports/validation_report.txt`
