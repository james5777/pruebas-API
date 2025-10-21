import requests
import datetime
import pandas as pd
from pathlib import Path
import sqlite3

# ------- Parametros editables ------- #
start_date = "2025-10-01"
end_date = "2025-10-20"

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_sportradar = "general_sportradar"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_sportradar = Path("Archivos/Archivos_csv/reporte_sportradar.csv")


# ------- Token de acceso y de refresco ------- #
id_token = "eyJraWQiOiJsMDdheTRNdEhWTWEwTDdvZEVReUorNUg1OHI1R2syaU1lK0dORTNCenV3PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoick9wLW5HcnMtN0J0ellMVWhKWl9fQSIsInN1YiI6IjRiZTZjODhlLWI1NWUtNDU5YS1hY2IxLWY1NWIxYzY3MDE4ZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9XNWF4YWFxMWwiLCJjb2duaXRvOnVzZXJuYW1lIjoiNGJlNmM4OGUtYjU1ZS00NTlhLWFjYjEtZjU1YjFjNjcwMThkIiwib3JpZ2luX2p0aSI6IjJlZWEwOWVhLWQ4ZDEtNGJmOS1hMmMwLWI4ZTZmMjI4MTYxMSIsImF1ZCI6IjF0YzM3aTVvaWhucjA0YmNpcTMzMzBkbHRvIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NjA2NDU3MjgsIm5hbWUiOiJUaGVvZG9ybyIsImV4cCI6MTc2MDczMjEyOCwiaWF0IjoxNzYwNjQ1NzI4LCJmYW1pbHlfbmFtZSI6IkRpa3V5YW1hIiwianRpIjoiZDY4NTgyYTYtZThjNS00YTUxLTlhZmMtZTNlNzhhMzA3ODk3IiwiZW1haWwiOiJ0aGVvZG9yby5kaWt1eWFtYUBxdW90YW1lZGlhLmNvIn0.uKChBlVR-upQdMdRvsgIHPlKbCYbnUGs4Lo7LLwirJAm2VZE06gSOPRbGtbzNnoG8ck2cx6Kv8BK_sC3jhiP2Sk9wXSZPUh029VPvI_8iriOi2CvpmM7Np7tg6EFvNX-YcZx32MjVJ1g7ZmgaqZaUiyDdTUqKT3KClIkGnIWG-F2Ign3qOnDu4Pl-kd8UNDCrJn5B1vCfvknIXSEjPa79OsLPgyBbtiB2UcJr9Sw5Bif8vkdsON1nLGEUxXm1Xzqrt-P7lkyIRUlsGemyb_qXV1qLvXuG8t2wrLTfypEVKdAyosi4nDmdYNwW8OLJk5cs6zG6fmKnGFmDXAKQPTsUw"  # token actual
refresh_token = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.UGTPdHE8WMauuUrbOloUEpJWX5Z7b3dpITMiyhFxLD9457PxICnOl9crgR67UN3OKafTJmRFiOVfgFIML5gfKc9qejSMDPGKvSLtavIe1VZQF22HXFhd5zOhrBGjAxqA-JSBLd92eYXD4dvmck15LYGj7axXtDu36KZy070ViO0OOHpdpl1x7vsl_eURWa_ZEx0FSm4k4dzKDKXO4-peUBLOw3kDjNWoChF31N948gMORHJyT4N0NDg-EGUhJ4BZqzATj-JWfTo8iEEyGWCggFoVLsgb3JUKyVshGKXPj3OFcBxlxzBs7KiG05uBd00OXPXEveNi370gLiXeO_FaSA.uduT6G_9aO3rDFYB.Yz2TXex5rE3M5eT6F7xKi_wvInTZmVJ_NWgSAn-T2DiwTu2OjKXWHTt3_K_hrAdNig5QuADRF9werpu7ox1bamJJSfdIJSkZONxPi5pxaXePrdwVpTaUZnkXDqoStHOgxddTmItxDFbplV9ytsE6JaVKjHZAvWz9nIX3GlGbLi6KQXyxbmKFp-0zowTVWF1KEYnOwP09wOBiNPydeDeDgj6AHSPndSl1Fvz79bT6j9C0d8PKScFK-Pl9nxRH_ZJmvHX7CWJd13hea6nl800OfocodFtzIAyy7A8cx7cmHSQbVN_-uIMnoC9_0W0T1GVp9hHwQ-AVcmlPAWKrIWDsgWZdZUsRmI6nUnibuw4InzSVlz8t7cicRHUT_jzj8yTHYySQgbDnFBv8L2O1tc7zXgHrihI9Db4thLrLaLHkedteXYAGeH8p2x2pUFiipXJBb2z8KdpSGiDDzqTDDYX352pI8nJPksyJ71pII36Dr8bMG8gkriGZg6SKq2hRMMAHKS4vrA01dW7sByvgLYKiwtzyo4nhipAzpZoF_Rmmv6TOZa7XuYdXz90WfRqqtB-8s4kq2a6Ya7UNGEO-kC4JbD4LnJvDXpQpt9uo2bC6d_RokMAfO5-E3T8C7NAVe6iFpmUdu13OIUimLuhoRZ5BHriROFM30vOCPHOFdqak73l7uS0c6f8M-mtm-M_r0Ct0Jku0666orD9i1fu5CF3bpF4H7OrExFcR-2YUSxA-Ddxn4LhQgfELgOn9f9GE_HasLBYNh0s_6CL7f9eZA3vvlcfakNvq_soDcBRa_PObA0AnTvExDK_8X417UIMtea1gz8VvT3dkN_zHkmPtOTxJSpQ935BUdgGmplnDwqZMnQCaeImehjghVi4xPG8LC8_dRe-nE12sqMToyhmcRCiFN_Wi84Op97ZEapYVVhldtE_wp-vlp1XjyhMBlR6V6NPewiGhGjcwGpMQ3isx6RHHoOlIttUE465yKPpYupQAgDbJD2lFdzEmWBQ1ZXX9Bdn6TYC6KGPVKk7ezw_eJnJ1IqxzGtE1m-VgHWkDyWi3LDC-dxGjGhWIWjFeiwxRRnBvFoAIBJMTe2P0Pncy6iOpNL9QBD1oBySEXF-YWpbRSSsogCODNT02EiZej_kqvq3rkVwvOcw_QfZZ4LeLwiOolpQqKWMgBF37_fLJIWxLeAJQFD44ow-yQOZwqLYU-4ZQq-UgCh9SNpIOA86wtJIEB-USAn2-xQ768qCiYUnh-6DAXdHOxMjPSQS0A4aaDG_OcOI.zE-P63lA7Qnm2mDsC4m1Dw"  # lo que te da el sistema al generar el token
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
        "pixel.type.login" ### Pixel inicios de sesion ###
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

