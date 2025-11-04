import requests
import pandas as pd
import json
import sqlite3
from pathlib import Path

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_propellerads = "general_propellerads"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_propellerads = Path("Archivos/Archivos_csv/reporte_propellerads.csv")

# -------- Token de acceso ------- #
TOKEN = "5e6cae2a20cdcda167cd0437d3097da7c1a92758f9c3c2ed"

# -------- EndPoint para informe granulado ------- #
API_URL = "https://ssp-api.propellerads.com/v5/adv/statistics"

# -------- Headers y autorizacion ------- #
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {TOKEN}"
}

# -------- Parametros generales ------- #
# -------- Parametros de fecha ------- #
day_from = "2025-10-01 00:00:00"
day_to = "2025-10-14 23:59:59"

# -------- Parametros de agrupacion y fecha ------- #
params = {
    "group_by[]" : ["date_time", "country_id", "campaign_id"],
    "day_from" : day_from,
    "day_to" : day_to,
}

# -------- Peticion a la API ------- #
print("🔄 Consultando estadísticas de PropellerAds...")
response = requests.get(API_URL, headers=headers, params=params)
print("Código HTTP:", response.status_code)

# -------- Validacion: Si el status_code es 200 entonces... ------- #
if response.status_code == 200:
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        # -------- Convertir a DataFrame ------- #
        df_propellerads = pd.DataFrame(data["items"])

        # -------- Ordeno por primero fecha y luego por nombre de campaña ------- #
        df_propellerads.sort_values(by=["date_time","campaign_name"], inplace=True, ignore_index=True)

        # -------- Mostrar primera data ------- #
        print("\n📊 Primera data obtenida:") 
        print(df_propellerads.head())

        # -------- Convierto el dataframe a CSV ------- #
        df_propellerads.to_csv(name_csv_propellerads, index=False, encoding="utf-8-sig")
        print(f"📁 Reporte guardado en '{name_csv_propellerads.name}'")
    else:
        print("No se encontraron datos en el rango de fecha especificado")
else:
    print("Error al consultar la API ❌")
    print(response.text)
    
# -------- Funcion para guardar en SQLite ------- #    
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
    # Validar que el DataFrame esté vacío.
    if df.empty:
        print(f"\n ⚠️ El DataFrame está vacío. No se insertaron datos en la tabla '{nombre_tabla}'.\n ")
        return
    try:
        # Conexión a SQLite
        with sqlite3.connect(ruta_db) as conn:
            df.to_sql(nombre_tabla, conn, if_exists=if_exists, index=False)
        print(f"\n ✅ Se insertaron los datos con la tabla '{nombre_tabla}' en la base de datos '{ruta_db.name}'.\n ")
    
    except Exception as e:
        print(f"\n ❌ Error al guardar en SQLite: {e}")

# -------- Se guarda el DataFrame en SQLite ------- #
guardar_en_sqlite(df_propellerads, nombre_tabla_propellerads, ruta_db, if_exists="replace")






