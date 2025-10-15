import requests
import datetime
import pandas as pd
from pathlib import Path
import sqlite3

# ------- Parametros editables ------- #
start_date = "2023-05-01"
end_date = "2025-10-14"

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_sportradar = "general_sportradar"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_sportradar = Path("Archivos/Archivos_csv/reporte_sportradar.csv")


# ------- Token de acceso y de refresco ------- #
id_token = "eyJraWQiOiJsMDdheTRNdEhWTWEwTDdvZEVReUorNUg1OHI1R2syaU1lK0dORTNCenV3PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiT1lOMEhvNEVLOUlpMTlrS0FEdW44dyIsInN1YiI6IjRiZTZjODhlLWI1NWUtNDU5YS1hY2IxLWY1NWIxYzY3MDE4ZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9XNWF4YWFxMWwiLCJjb2duaXRvOnVzZXJuYW1lIjoiNGJlNmM4OGUtYjU1ZS00NTlhLWFjYjEtZjU1YjFjNjcwMThkIiwib3JpZ2luX2p0aSI6IjQ0N2EzOTM3LWJiNzUtNGE0Ny04OTZhLWU1NDE4OWFlYmNiMSIsImF1ZCI6IjF0YzM3aTVvaWhucjA0YmNpcTMzMzBkbHRvIiwiZXZlbnRfaWQiOiJmOWE1MGJiNS03Y2YyLTRjN2QtYjY1MS1mNWViMWY5YjcyMWUiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTc2MDU1MTE1MSwibmFtZSI6IlRoZW9kb3JvIiwiZXhwIjoxNzYwNjM3NTUxLCJpYXQiOjE3NjA1NTExNTIsImZhbWlseV9uYW1lIjoiRGlrdXlhbWEiLCJqdGkiOiJlMDc2MzRiZS1jMmIwLTRlMTktYjUxNC0wYjEyNmJkOWZhMWQiLCJlbWFpbCI6InRoZW9kb3JvLmRpa3V5YW1hQHF1b3RhbWVkaWEuY28ifQ.FWGmnkrvHMWOxluIZnzULX1L9qZYofazEgVi3ZmuUaI7BjmSDx7HPoWeIanZdBW1ypbPh7y2aMKEseHSABsASFmHNXvJ9VlmFgd-LiGR8jXfqNEAmFISR8JbZL-X1cZjoYf5MnVupxfUzBzK-dXTTnx7ak0UNUJ1hNscr-NT1Sjy9c0be3FitAbg2P57-OK3rkTpTiWQooh0OvP-mOCh0E4GNjyINecKP1hSN7xMOH8o-4GH9j2cEUlwETkudGf4RGrblcsZfxM3Y63ScENtNW3gnagtkBiCHAthilTkZ_warB-SjDwuo-k3IH1NujFl7jpR-bdrCl2yBUNxDFAYGA"  # token actual
refresh_token = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.EAXqFeYfzEQwhD0MZEAiuRx6Fq-knbRq3qm8uklosY4tKxuuxTpoelGSOGOG8cS3m0R7y-KvjpwpbZ6jxEYa_fxgHTIAwc1JXnsgDWfhTt2Uf-QEOw85KK7ow_MWgx-FOcyB4ftMVlK_UEt_0Oce3Y36dbrV_KVFEQJiaqz_q8Jnfs9NtmKk4s-vpp7aTlWrvDPvg335Gmhb7JjPIqlCbfS2NHzh9OHUjZ-O4upYjqtDhWnKRzI4LBkaX27jsdryPOT4J0iMOFpo4e3uLc-Tr80fBFVb_e87GVI4HU_HJThJkg3wzrXwfCeAdfIxz1aYtxiWJytQokyQaRGXrZ-F4g.eURLd6lqca4b6V7s.Esug-5Q0EoPCIH2JuLlTXj5RkBXTKXV8qTNzKoUnQL_Jge9dEX6gnGJ1OUm5Yl-IM8q6cmw23zfkLtyPikWVlEVBNU0AHTafUeQGBMNb6fDyuhQ_Gaut-eDC3Knd1Aj9MAL6Tbp5VuRpBt__L_tdBNE3b6JF71hEDmW9jlqFElLDHJYiUKIA93uHNwegDnaI6H9WgrxK39LA1nk4FxAs8hjZjBSs4pZPNKu7pQGo_NyHOXQOBTN-jCI-zNUBDHwxxuzpsemYmHetnhJ4IBRE9lxfKjTJmS8YZh2F6zb7ci7XeQLt_Nri8nne5OsDMgUEnT_sYEEm4Rv7NvNqa5XAU1G3VSWsI6LJXa5baWMzviGe_lDjGGEnPpVz_mY7jyZQMY6SJgreaV5e3r0yvSnVFJiHP9g7YCsJ3t0a7TgDfLZPtWth4uBgrFkPwgrQ_Yo3QKgJHGfOzOASIh9u7aJzUHRiytGHZlbnrSb5p7y5zOGB05aiQCwF5REKCRKU4jKn2NJ8M36WdS3kW2AL7cCvVvGBEebIbR2WbF2UES7a3aVR4IUVbnN89NtkFLY6PG0QuojONnFgGwy7rl-1LwX00ZvDcH0AdrLpbGVmQv-8OjEnR2DVHhqe4DElCg65u4vgC0fzessdAdKe23WdztIZBv1dpfi9PDQXvWTfl4kZp3dRI01qJkjl2Pi-31CN9715_H_QOMONjSzPN36rLfX9wOrzGjeE-G068bjmDCXkUJVfytG4sXxpucYcFsbKaQciE0ju7r4odWnQjUKJPfanBcyoQ8JQEk5mtDCYo5_Eu-naNaAy0wij1TpMKDM7fDauYBuMjuSeVHWduf0MFtLpnFDkgze4Kxdix2n0U8pzriTJTW-6PNM8ZGRUsyOmT4DJIw0IOoZplEyuInKuQIeTeq47caiRGqPrO72nOSLHX05_AChVVcwLYnhPoIKD03HVHvqvg9wNCCRb30ybm6TweWW7kogomjEgDY-W_Zk2zYj8JbfEo5_N3-8sfH-gopBF1EUQZPP6uJlwPJUtQoVO-TZqwqiVlhDZKzmf9HaQRhQ1QMNtDzk-8RIyNI98vSvyu7f93qKkty9tMrg2KWfhWfUoMrmVQlbDUXEk6oXH2k46A7tdYhMDFP7YDazOia7v1q0UKVQ0QMvhzmrqEn12XEEeiKffXJTMbbYbVtriLuyTwxdQVMGCXs7iXfaQvpc4F4cPT8HEOima2Ba8Nn2LVAdPxKkUs6ECRDilsPVIN2RrABBJE08vQiq80uTzzpyjqi49fW1TBncKSOdGifL-Pjvr_sYvxYc0YpQ5d9bOTW3TcUfnTPiunP2oCucLAi0J_L1TR6KuT40IYt0bfuRn2O7c7dtQ.DET3WW4FGzMrmgIqkLwasQ"  # lo que te da el sistema al generar el token
token_expiration = datetime.datetime.now() + datetime.timedelta(hours=6)

# ------- Funcion que usa el token de refresco para actualizar el token ------- #
def refresh_id_token():
    global id_token, token_expiration
    url = "https://api.api-access.iam.ads.sportradar.com/prod/oauth2/token"
    headers = {"Authorization": f"Bearer {id_token}"}
    body = {"refreshToken": refresh_token}
    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        new_data = response.json()
        id_token = new_data["idToken"]  # nuevo token
        token_expiration = datetime.datetime.now() + datetime.timedelta(hours=6)
        print("✅ Token actualizado correctamente")
    else:
        print("❌ Error al renovar token:", response.text)

# ------- Funcion para verificar si ya pasaron 6 horas desde la ultima vez que se ejecuto el token ------- #
def get_data_from_api():
    if datetime.datetime.now() >= token_expiration:
        refresh_id_token()

    headers = {"Authorization": f"Bearer {id_token}"}
    url = "https://api.reporting-studio.ads.sportradar.com/..."  # endpoint específico
    response = requests.get(url, headers=headers)
    return response.json()


# ------- Parametros para la consulta en la API ------- #
url = "https://api.reporting-studio.ads.sportradar.com/grid"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {id_token}",
    "Content-Type": "application/json"
}

# ------- Parametros de agrupacion por advertiser, id de campaña, pais, granularidad(DIA) ------- #
body = {
    "split_by": [
        "demand.advertiser_id", ### ID de anunciante ###
        "demand.campaign_id", ### ID de campaña ###
        "user.geo.country", ### Pais donde se visualizo ###
        "granularity_day", ### Granularidad (Dia) ###
        # "conversion_id"
    ],

    # ------- Parametros de rango de fecha ------- #
    "start_date": start_date, ### Fecha de inicio ###
    "end_date": end_date, ### Fecha final ###

    # ------- Metricas ------- #
    "data_fields": [
        "payout.actual_adv_usd", ### Gasto en dolares ###
        "clicks", ### Clicks ###
        "imps", ### Impresiones ###
        "pixel.type.ftd", ### Pixel primeros depositos ###
        "pixel.type.reg_finished", ### Pixel registros finalizados ###
        "pixel.type.deposit", ### Pixel depositos ###
        "pixel.type.login", ### Pixel inicios de sesion ###
        "pcc_amount", ### Conversion post clic ###
        "pvc_amount" ### Conversion post view ###
    ]
}

# ------- Limite de filas ------- #
body["limit"] = 100000 

if datetime.datetime.now() >= token_expiration:
    refresh_id_token()

# ------- Peticion a la API ------- #
response = requests.post(url, json=body, headers=headers)
data = response.json()

# ------- Procesamiento de datos ------- #
rows = []
# ------- Se relaciona los diccionarios que vienen en "name" como columnas ------- #
for row in data.get("rows", []):
    record = {
        "advertiser_id": row["name"][0],
        "campaign_id": row["name"][1],
        "country": row["name"][2],
        "day": row["name"][3],
        # "conversion_id": row["name"][4],
    }

# ------- Se relacionan los diccionarios que vienen en "Data" con los diccionarios que vienen en "name" ------- #
    for metric in row.get("data", []):
        metric_name = metric.get("name")
        metric_value = metric.get("value")
        record[metric_name] = metric_value

# ------- Se agregan los diccionarios(filas) a la lista record ------- #
    rows.append(record)

# ------- Se crea un dataframe con cada fila de record, donde la clave es el nombre de la columna y el valor es el registro ------- #
df_sportradar = pd.DataFrame(rows)

# ------- Se calculan metricas adicionales ------- #
if not df_sportradar.empty:
    df_sportradar["CPL"] = (df_sportradar["payout.actual_adv_usd"] / df_sportradar["pixel.type.reg_finished"]).round(2)
    df_sportradar["CPA"] = (df_sportradar["payout.actual_adv_usd"] / df_sportradar["pixel.type.ftd"]).round(2)
else:
    print("⚠️ No se encontraron registros en el rango de fechas.")

# === 7️⃣ Guardar resultados ===
df_sportradar.to_csv(name_csv_sportradar, index=False)
print("✅ Datos guardados en 'reporte_sportradar.csv'")
print(df_sportradar.head())

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

guardar_en_sqlite(df_sportradar, nombre_tabla_sportradar, ruta_db, if_exists="replace")

