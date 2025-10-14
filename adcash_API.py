import requests
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import sqlite3

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_ad_cash = "general_adcash"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_ad_cash = Path("Archivos/Archivos_csv/reporte_adcash.csv")

# ------- Credenciales de acceso ------ #
USERNAME = "digital@quotamedia.co"
PASSWORD = "Quota.media2022"

# ------- Parametros para obtener el token de acceso ------ #
auth_url = "https://api.myadcash.com/api/v1/auth/"
auth_data = {"username": USERNAME, "password": PASSWORD}
auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)
auth_response.raise_for_status()

# ------- Se hace la peticion del token ------ #
token = auth_response.json().get("token", "").strip()  # 👈 importante: limpia espacios
print("✅ Token obtenido correctamente")


if not token:
    raise ValueError("❌ No se recibió token válido")


# ------- Parametros y EndPoint para el reporte ------ #
report_url = "https://api.myadcash.com/api/v1/advertiser-report"

# ------- Se ingresa la fecha de inicio y fecha final ------ #
start_date = "2025-10-01"
end_date = "2025-10-13"

params = {
    "start_date": start_date,
    "end_date": end_date,
    "advertiser_id": "174198",
    "group_by": "date,country,campaignname" # Se puede agrupar por maximo 4 parametros

}
# ------- Parametros para agrupar ------ #
#date,country,campaignid,campaignname,devicetype,packid,packname,platformname,browser,zoneid

# ------- Autorizacion para reporte ------ #
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# ------- Se hace la peticion del reporte ------ #
response = requests.get(report_url, headers=headers, params=params)
print("🔎 Status code:", response.status_code)
print("🔎 Respuesta:", response.text)  # 👈 ver respuesta real

if response.status_code != 200:
    print("❌ Error al obtener datos:", response.text)
else:
    data = response.json()
    if isinstance(data, list):
        df_ad_cash = pd.DataFrame(data)
    elif "data" in data:
        df_ad_cash = pd.DataFrame(data["data"])
    else:
        raise ValueError("❌ La respuesta no contiene datos tabulares válidos")

    print("✅ Datos recibidos correctamente")
    print(df_ad_cash.head())

    # ------- Se guardan los resultados en un archivo CSV ------ #
df_ad_cash.to_csv(name_csv_ad_cash, index=False, encoding="utf-8-sig")
print(f"📁 Reporte guardado en '{name_csv_ad_cash.name}'")

# ------- Funcion para guardar en SQLite ------ #
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

# ------- Se guarda el DataFrame en SQLite ------ #
guardar_en_sqlite(df_ad_cash, nombre_tabla_ad_cash, ruta_db, if_exists="replace")