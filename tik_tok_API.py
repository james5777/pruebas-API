import requests
import json
import pandas as pd
from pathlib import Path
import sqlite3
import re
from datetime import datetime

print("Iniciando proceso de obtencion de datos de la API de Tiktok...")

# ------- Parametros editables ------- #
start_date = "2025-10-01"
end_date = "2025-10-14"

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_tiktok = "general_tiktok"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_tiktok = Path("Archivos/Archivos_csv/reporte_tiktok.csv")

# ------- Variables para nombres de columnas ------- #
name_column_fecha = "Fecha"
name_column_partner = "Partner"
name_column_pais = "Pais"
name_column_inversion = "Inversion"

# ------- Nombres de partners ------- #
name_partner_ecuabet = "Ecuabet"

# -------- Nombres de paises ------- #
name_pais_ecuador = "Ecuador"

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

else:
    print("❌ Error en la respuesta de la API:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

print("Dataframe inicial recibido desde la API de tik tok")
print(df_tiktok.head())

# ------- Normalizacion de columna stat_time_day ------- #
df_tiktok["stat_time_day"] = pd.to_datetime(df_tiktok["stat_time_day"]).dt.strftime("%y-%m-%d")

# print("Dataframe con la columna fecha normalizada")
# print(df_tiktok.head())

################################################
####### Sección de diccionarios de mapeo #######
################################################

mapeo_partner = {
    # Ecuabet
    r'ec|none' : name_partner_ecuabet
}

mapeo_paises = {
    # Ecuador
    r'ec|none' : name_pais_ecuador
}

###############################################
###### Fin seccion diccionarios de mapeo ######
###############################################

# ------- Normalizar columna country_code ------- #
df_tiktok["country_code"] = df_tiktok["country_code"].str.lower().str.strip()

# ------- Crear una columna Partner y mapear valores de la columna country_code ------- #
df_tiktok[name_column_partner] = (
    df_tiktok["country_code"]
    .apply(lambda x: next((v for k, v in mapeo_partner.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
)

# print("Columna Partner creada correctamente.")
# print(df_tiktok.head())

# ------- Crear columna Pais y mapear valores de la columna country_code ------- #
df_tiktok[name_column_pais] = (
    df_tiktok["country_code"]
    .apply(lambda x: next((v for k, v in mapeo_paises.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
)

# print("Columna Pais Creada correctamente.")
# print(df_tiktok.head())

# ============================================================
# ------- Conversion de COP a USD ------- #
# ============================================================

# ------- Se crea una nueva columna con donde multiplica la cantidad en pesos, por el valor del dolar del dia ------- #

def obtener_tasa_cambio_cop_usd():
    """
    Obtiene la tasa de cambio actual de COP a USD usando exchangerate-api.com
    
    Returns:
        float: Tasa de cambio COP/USD, o None si hay error
    """
    try:
 # ------- EndPoint de conexion para consultar TRM ------- #       
        url_exchange = "https://api.exchangerate-api.com/v4/latest/COP"
        response = requests.get(url_exchange, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            tasa_usd = data['rates']['USD']
            print(f"💱 Tasa de cambio obtenida: 1 COP = {tasa_usd} USD")
            return tasa_usd
        else:
            print(f"⚠️ Error al obtener tasa de cambio. Código: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error al consultar API de tasas de cambio: {e}")
        return None

# ------- Se obtiene el precio del COP en USD ------- #
tasa_cop_usd = obtener_tasa_cambio_cop_usd()

print(f"El valor del COP es de ${tasa_cop_usd} USD")

if tasa_cop_usd:
    # ------- Convertir la columna 'spend' de COP a USD ------- #
    df_tiktok['spend_usd'] = df_tiktok['spend'].astype(float) * tasa_cop_usd
    
    # ------- Se redondea a 2 decimales ------- #
    df_tiktok['spend_usd'] = df_tiktok['spend_usd'].round(2)
    
    # print("✅ Columna 'spend_usd' creada exitosamente.")
    # print(f"\nPrimeras filas con la conversión:")
    # print(df_tiktok[['stat_time_day', 'spend', 'spend_usd']].head())
else:
    print("⚠️ No se pudo crear la columna 'spend_usd' por falta de tasa de cambio.")
    # Crear columna con valores None o 0 para mantener estructura
    df_tiktok['spend_usd'] = None

# ============================================================
# ------- Fin de conexion con la API de TRM ------- #
# ============================================================

# print("dataframe con trm USD-COP")
# print(df_tiktok.head())

# ------- Se renombran columnas ------- #
df_tiktok.rename(columns={
    "stat_time_day" : name_column_fecha,
    "spend_usd" : name_column_inversion
}, inplace=True)

# print("Columnas renombradas correctamente.")
# print(df_tiktok.head())

# ------- Se crea un DataFrame final solo con las columnas necesarias ------- #
df_final_tiktok = df_tiktok[[name_column_fecha, name_column_partner, name_column_pais, name_column_inversion]]

# print("Dataframe final con las columnas necesarias.")
# print(df_final_tiktok.head())

# ------- Se agrupa el dataframe por fecha, partner y pais y se suma la columna inversion (en dolares)------- #
df_final_tiktok = df_final_tiktok.groupby([name_column_fecha, name_column_partner, name_column_pais], as_index=False)[[name_column_inversion]].sum()

print("DataFrame final con las columnas necesarias y agrupado.")
print(df_final_tiktok.head())

# ------- Se guarda el dataframe en un archivo CSV ------- #
df_final_tiktok.to_csv(name_csv_tiktok, index=False, encoding="utf-8-sig")
print(f"📊 Archivo {name_csv_tiktok.name} guardado correctamente.")

# def guardar_en_sqlite(df: pd.DataFrame, nombre_tabla: str, ruta_db: Path, if_exists: str = "replace") -> None:
#     """
#     Guarda un DataFrame en una base de datos SQLite, creando o actualizando la tabla según se especifique.

#     Parámetros:
#     ----------
#     df : pd.DataFrame
#         El DataFrame que se desea guardar en la base de datos.
    
#     nombre_tabla : str
#         El nombre de la tabla en la base de datos SQLite.
    
#     ruta_db : Path
#         Ruta al archivo `.sqlite` o `.db` donde se guardarán los datos.
    
#     if_exists : str, opcional
#         Comportamiento si la tabla ya existe. Valores permitidos:
#         - 'replace' (por defecto): elimina la tabla y la vuelve a crear.
#         - 'append': agrega los datos sin eliminar la tabla.
#         - 'fail': lanza una excepción si la tabla ya existe.

#     Retorna:
#     -------
#     None
#         Esta función no retorna un valor. Inserta los datos directamente en la base de datos.
#     """
#     # Validar que el Dataframe no esté vacío
#     if df.empty:
#         print(f"\n ⚠️ El dataframe está vacío. No se insertaron datos en la tabla '{nombre_tabla}'.\n ")
#         return
#     try:
#         # Conexion con SQLite
#         with sqlite3.connect(ruta_db) as conn:
#             df.to_sql(nombre_tabla, conn, if_exists=if_exists, index=False)
#         print(f"\n ✅ Se insertaron los datos en la tabla: '{nombre_tabla}' en la base de datos '{ruta_db.name}'.\n ")
    
#     except Exception as e:
#         print(f"\n ❌ Error al guardar en SQLite: {e}")

# guardar_en_sqlite(df_tiktok, nombre_tabla_tiktok, ruta_db, if_exists="replace")