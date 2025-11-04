import requests
import datetime
import pandas as pd
from pathlib import Path
import sqlite3

# ------- Parametros editables ------- #
start_date = "2025-10-15"
end_date = "2025-10-25"

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_sportradar = "general_sportradar"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_sportradar = Path("Archivos/Archivos_csv/reporte_sportradar.csv")


# ------- Token de acceso y de refresco ------- #
id_token = "eyJraWQiOiJsMDdheTRNdEhWTWEwTDdvZEVReUorNUg1OHI1R2syaU1lK0dORTNCenV3PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiZkZKUnFia2ljZUh0Wk5WSGUxQ0RNZyIsInN1YiI6IjRiZTZjODhlLWI1NWUtNDU5YS1hY2IxLWY1NWIxYzY3MDE4ZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9XNWF4YWFxMWwiLCJjb2duaXRvOnVzZXJuYW1lIjoiNGJlNmM4OGUtYjU1ZS00NTlhLWFjYjEtZjU1YjFjNjcwMThkIiwib3JpZ2luX2p0aSI6ImE3MzliNGM3LTA4NDYtNDkwOS04NDQxLTMyZDE0YzI2YjY5YyIsImF1ZCI6IjF0YzM3aTVvaWhucjA0YmNpcTMzMzBkbHRvIiwiZXZlbnRfaWQiOiI5N2Q2MGRlMi1hZWUzLTQwMmItYTc4Mi1hN2JiNzdmNGFiNzMiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTc2MjI3NTUyOCwibmFtZSI6IlRoZW9kb3JvIiwiZXhwIjoxNzYyMzYxOTI4LCJpYXQiOjE3NjIyNzU1MjgsImZhbWlseV9uYW1lIjoiRGlrdXlhbWEiLCJqdGkiOiJlOTAzMjQxYS1jODAwLTRiODYtOWMwZi1kN2MxODA4YTdlMzAiLCJlbWFpbCI6InRoZW9kb3JvLmRpa3V5YW1hQHF1b3RhbWVkaWEuY28ifQ.gOKoclT4eAI_rN_0OJkOIgmB6oNjpAAZNfvRnx50Y8DzkJuyU7DIq_6gm6e5Z6cZ83x51ZUVzvRs0lm3qHyga1yr6TcTRwzASpbeNu8tJfs3Y-zZY7MgOdpo8Gi2CRRtOJUdyBu6Vzz-CcF6V6uaaqbWJw9htSex0RqZDx4U2CWXNaxJkjUN85vtoU-FeYGd_tBACCHZWjAhf2HdMBvSvIfTspBuJr1ps_mQNQKoC4HJ3i-4IwAQWg-SQA4UZbzqsnjGxW6dUnafie85btk5T7cRmJMOvd8AymJIu-kyWIbjQGYIgBzIHRknpInUtEukgWCFZpixgvRctZOQfpYrhA"  # token actual
refresh_token = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.VgyhxxJc5wmBBy0EIQoPCZAlB9-kaBrJXirUOccRVk3fWwAnrf7HXbEW5qRxHe9QmkdSvKWD5NtQZOKRab-ZVLeVVl9Wdb33N26UG9EbrvUuVSYezPbw4GufITuvS4vq-12IJcdhhl8kr7-1qTEG-D2BXOloIzwKGbKwmD1xSyzvSGXaKC1tlf2pyLeSKsMNOEFoWsC-gJsJ85JHNG1XsF-HAtVFuyV7p9RXF213bi7OrEy9F4T6QYF9d-AZntN6DSXt07hwNG19v3IZQH9nUagUwfvOVbyd7S0YzN2vWglqnsMfjd1zLW892ejDRpyOrlmw337HmKExHcGBaXgiAg.fU_34a5afeWgME_6.384niRwMnrIbSCX5tgpCMTR_vC1HeyV0B6OZz6BJpEFTpGn0D0u6_ifdQLlIBf0gqxrT5jRPqW-pW18ShWGPNroszY96u0uojRp16KD0VTqUAVi73wNNdLqgKHgndiwPHZLB70kU4aGG0A6POzmclZW50YTLmcWQLZa5Ia6zq7QSVcEumiDuR7t_Ok1wx3LIahqN4SHw1qr9A-oOz3QEnns113OlCvIXyhpYeHvGowhgOEVW-EcG3crKPSSuyynqA5QXohE6KIX2dj4HmQ0Dv9m6LGu8jmSK0XbCDvETQoT4moeMU-hl5stsCyVa-9AbQQtkDVyu2eKSIeewZiaigoeTR9I8Mj6-3PbTqhEmDleq2A_kLO69hwjw-KvhWkd7Jmb2x04Q5LjdLv9KaOCmJ3Io0rlxbKEBzkCVoGbiVD-mE0nwe_BAIldlK7HGfGBwfSi48-EsqmxESWTbBGFoSyZSUjCBCZH_sVHuXlJvxcXc3eE60gUQtrGUL_-gusATf3LIcXy_OWJJeu_kIPKmTG-cF_WL3qQBcUfOeBfo9s-bLVpOj1hCjEQImK8c5YRVtX_s5Ml0KUGiBG4VnY-QdbQvwiR7XowdGKwnNMwq39WRodzQr0VeaMuyVX7ibBsCZKLtKO-iV7bCd6KVVGDHsrEOXoIbq7tnkJawCV2l6Np8_CJoG8mNm7yr5idDfnEMkZK5DTddYCWmE0U8B-2jUavBYiOp4kdxCGGOCMn9TdLeIb7gvx1HcJcj2HOJ3tZ7jrnyLo5sMKihVMs43kCf-Ssx6p2JmV2Pi2bN4XNiAuN3i_AQ9Po0vKNbUeGvekpGFws-_uzEoQcWjLkJwOYq4U1RqewVEE58eA2rBfhDGVFgz6_3qFV9VZcjlhvuKadmK8MaA-3PejXkuK9Zval_EpHQm8nPOT3SYCh0vgeaGQ1rEi7NWgf2zm79wDg0NiaBECGBoe1HZhickEZgH1hEm3O1WH6VQKBVBE10DS0bIsUq7z8v3hFXT96puVzOiVrwvjnxADUXObD9AISWelhdneEZ37McxWQbdCmdg4_GTS2_J899OPjkfvXG-lygCiJCyhKJU1t8ZzEelYQrA-gxlS7F5KF7DwtonYn7cxAc_MW-KN7RlCBo-IZE5IztKusKjUL3xMWfRM0KCImHpDw0By8pkPeIOU_yDng4VN5nXLEjyJjhADTgvnvSheHvsmRQ1O0NFO7ZR5J64FwX1VezcOU2Ehhq7sjyOJEwurpAxn6g6NlEd7D_zRnL_-LmmQ3AClBdw35eF1JcMQuRTuCu6Pee2RRIqBD0psHqRSYsDjGvz3_NH2cHo9_VTDuA3PkVzBu1KN-1FZpYTSs5RRlBJLLP7k6O.BfHhVH4cyA-s3skLOFz9bA"  # lo que te da el sistema al generar el token
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

# ------- Parametros de agrupacion por advertiser, id de campaña, pais, granularidad(DIA), ID de creativo ------- #
body = {
    "split_by": [
        "demand.advertiser_id", ### ID de anunciante ###
        "demand.campaign_id", ### ID de campaña ###
        "user.geo.country", ### Pais donde se visualizo ###
        "granularity_day", ### Granularidad (Dia) ###
        "demand.creative_id" ### ID de creativo ###
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
        # "pixel.type.deposit", ### Pixel depositos ###
        # "pixel.type.login" ### Pixel inicios de sesion ###
        # "pcc_amount", ### Conversion post clic ###
        # "pvc_amount" ### Conversion post view ###
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
        "creative_id": row["name"][4]
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

# ------- Se ordena el dataframe por dia y luego por pais ------- #
df_sportradar.sort_values(by=["day", "country"], inplace=True, ignore_index=True)

# # ------- Se calculan metricas adicionales ------- #
# if not df_sportradar.empty:
#     df_sportradar["CPL"] = (df_sportradar["payout.actual_adv_usd"] / df_sportradar["pixel.type.reg_finished"]).round(2)
#     df_sportradar["CPA"] = (df_sportradar["payout.actual_adv_usd"] / df_sportradar["pixel.type.ftd"]).round(2)
# else:
#     print("⚠️ No se encontraron registros en el rango de fechas.")

# === 7️⃣ Guardar resultados ===
df_sportradar.to_csv(name_csv_sportradar, index=False, encoding="utf-8-sig")
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

