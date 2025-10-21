import requests
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import sqlite3

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_mgid = "general_mgid"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_mgid = Path("Archivos/Archivos_csv/reporte_mgid.csv")

# === ⚙️ CONFIGURACIÓN GENERAL ===
API_ID = "730589"  # tu APIId real
TOKEN = "06426fb424b53f2e9b3753a6694f7ef2"  # tu token válido

API_URL = f"https://api.mgid.com/v1/goodhits/clients/{API_ID}/statistics-reports"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# === 📅 RANGO DE FECHAS (en formato ISO 8601) ===
date_from = "2025-08-01"
date_to = "2025-10-19"

# === ⚙️ DIMENSIONES Y MÉTRICAS ===
# Puedes agregar o quitar fácilmente
dimensions = ["day", "source", "campaignName"]
metrics = [
    "spent", "clicks", "revenue",
    "profit", "conversionsDecision", "conversionsBuy"
]

# === 🔧 PARÁMETROS ===
params = {
    "filters[dateRange][dateFrom]": date_from,
    "filters[dateRange][dateTo]": date_to,
    "limit": 5000  # MGID máximo 5000 por página
}

# Agregar dinámicamente las métricas y dimensiones al query
for i, dim in enumerate(dimensions):
    params[f"dimensions[{i}]"] = dim
for i, met in enumerate(metrics):
    params[f"metrics[{i}]"] = met

# === 🚀 SOLICITUD A LA API ===
print("🔄 Consultando estadísticas de MGID...")
response = requests.get(API_URL, headers=headers, params=params)
print("Código HTTP:", response.status_code)

if response.status_code != 200:
    print("❌ Error al obtener datos:")
    print(response.text)
    exit()

data = response.json()

# === 📦 PROCESAR DATOS ===
if "data" not in data or not data["data"]:
    print("⚠️ No se encontraron datos para el rango de fechas dado.")
    exit()

# Convertir los valores anidados a algo plano
records = []
for item in data["data"]:
    row = {}
    for key, value in item.items():
        if isinstance(value, dict) and "amount" in value:
            row[key] = float(value["amount"])
        else:
            row[key] = value
    records.append(row)

# === 📊 CREAR DATAFRAME Y GUARDAR ===
df_mgid = pd.DataFrame(records)
df_mgid.sort_values(by=["day", "campaignName"], inplace=True, ignore_index=True)

print("\n✅ Muestra de datos obtenidos:")
print(df_mgid.head())

# Guardar a Excel con timestamp
df_mgid.to_csv(name_csv_mgid, index=False, encoding="utf-8-sig")
print(f"📁 Reporte guardado en '{name_csv_mgid.name}'")

def guardar_en_sqlite(df: pd.DataFrame, nombre_tabla: str, ruta_db: Path, if_exists: str = "replace") -> None:
    """
    Guarda un DataFrame en una base de datos SQLite, creando o actualizando la tabla según se especifique.

    Parámetros:
    ----------
    df : pd.DataFrame
        El DataFrame que se desea guardar en la base de datos.
    
    nombre_tabla : str
        El nombre de la tabla en la base de datos SQLite.
    
    ruta_db : Path
        Ruta al archivo `.sqlite` o `.db` donde se guardarán los datos.
    
    if_exists : str, opcional
        Comportamiento si la tabla ya existe. Valores permitidos:
        - 'replace' (por defecto): elimina la tabla y la vuelve a crear.
        - 'append': agrega los datos sin eliminar la tabla.
        - 'fail': lanza una excepción si la tabla ya existe.

    Retorna:
    -------
    None
        Esta función no retorna un valor. Inserta los datos directamente en la base de datos.
    """
    # Validar que el DataFrame no esté vacío
    if df.empty:
        print(f"\n ⚠️ El DataFrame está vacío. No se insertaron datos en la tabla '{nombre_tabla}'.\n ")
        return
    try:
        # Conexión a SQLite
        with sqlite3.connect(ruta_db) as conn:
            df.to_sql(nombre_tabla, conn, if_exists=if_exists, index=False)
        print(f"\n ✅ Se insertarón los datos con la tabla: '{nombre_tabla}' en la base de datos '{ruta_db.name}'.\n ")
    
    except Exception as e:
        print(f"\n ❌ Error al guardar en SQLite: {e}")

guardar_en_sqlite(df_mgid, nombre_tabla_mgid, ruta_db, if_exists="replace")