import requests
import json
import pandas as pd
from pathlib import Path
import sqlite3

# ------- Parametros editables ------- #
start_date = "2025-10-01"
end_date = "2025-10-14"

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_tiktok = "general_tiktok"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_tiktok = Path("Archivos/Archivos_csv/reporte_tiktok.csv")

# ------- Credenciales y token de acceso ------- #
ACCESS_TOKEN = "e5fc2d03f36ad3313f3895050ba9123070890785"
ADVERTISER_ID = "7416384907804442625"

# ------- EndPoint de informes de la API ------- #
url = "https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/"

# ------- Lista de todas las metricas de tik tok ------- #
all_metrics = [
    "spend", "impressions", "clicks", "reach", "conversion",
    "cpc", "cpm", "ctr", 
    "cost_per_conversion", "result", "result_rate", "conversion_rate",
     "video_watched_2s", "video_watched_6s", "likes", "shares",
    "comments", "profile_visits", "follows",
    "complete_payment", "currency", "campaign_id"
]

# ------- Parametros de la llamada a la API ------- #
params = {
    "advertiser_id": ADVERTISER_ID,
    "service_type": "AUCTION",
    "report_type": "BASIC",
    "data_level": "AUCTION_AD",
    "dimensions": json.dumps(["ad_id", "stat_time_day", "country_code"]),
    "metrics": json.dumps(all_metrics),
    "start_date": start_date,
    "end_date": end_date,
    "page_size": 1000
}

# ------- Encabezados de la consulta a la API ------- #
headers = {"Access-Token": ACCESS_TOKEN}

print("🔄 Consultando informe de TikTok con TODAS las métricas disponibles...")

# ------- Se hace la llamada a la API ------- #
response = requests.get(url, headers=headers, params=params)
print("Código HTTP:", response.status_code)

# ------- Se asigna la respuesta de la API a la variable "data" ------- #
data = response.json()

# ------- Se agrega cada fila del diccionario code, a la lista registros ------- #
if data.get("code") == 0:
    print("✅ Reporte obtenido correctamente.\n")
    report_list = data.get("data", {}).get("list", [])
    registros = []
    for item in report_list:
        fila = {}
        fila.update(item.get("dimensions", {}))
        fila.update(item.get("metrics", {}))
        registros.append(fila)

# ------- Se crea el dataframe a partir de la lista registros ------- #
    df_tiktok = pd.DataFrame(registros)
    
# ------- Se ordena el DataFrame por fecha y luego por codigo de pais ------- #
    df_tiktok.sort_values(by=["stat_time_day", "country_code"], inplace=True, ignore_index=True)
# ------- Se guarda el DataFrame en un archivo CSV ------- #
    df_tiktok.to_csv(name_csv_tiktok, index=False, encoding="utf-8-sig")
    print(f"📊 Archivo {name_csv_tiktok.name} guardado correctamente.")

else:
    print("❌ Error en la respuesta de la API:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

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
    # Validar que el Dataframe no esté vacío
    if df.empty:
        print(f"\n ⚠️ El dataframe está vacío. No se insertaron datos en la tabla '{nombre_tabla}'.\n ")
        return
    try:
        # Conexion con SQLite
        with sqlite3.connect(ruta_db) as conn:
            df.to_sql(nombre_tabla, conn, if_exists=if_exists, index=False)
        print(f"\n ✅ Se insertaron los datos en la tabla: '{nombre_tabla}' en la base de datos '{ruta_db.name}'.\n ")
    
    except Exception as e:
        print(f"\n ❌ Error al guardar en SQLite: {e}")

guardar_en_sqlite(df_tiktok, nombre_tabla_tiktok, ruta_db, if_exists="replace")
