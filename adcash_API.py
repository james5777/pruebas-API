import requests
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import sqlite3
import re

def obtener_datos_ad_cash() -> pd.DataFrame:
    print("Iniciando proceso de obtencion de datos de la API de Ad Cash...")

    # ------- Se ingresa la fecha de inicio y fecha final ------ #
    start_date = "2025-10-02"
    end_date = "2025-10-14"

    # ------- Nombres de variables para rutas y nombres de tablas ------- #
    nombre_tabla_ad_cash = "general_adcash"
    ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
    name_csv_ad_cash = Path("Archivos/Archivos_csv/reporte_adcash.csv")

    # ------- Variables para nombres de columnas ------- #
    name_column_fecha = "Fecha"
    name_column_partner = "Partner"
    name_column_pais = "Pais"
    name_column_inversion = "Inversion"
    name_column_plataforma = "Plataforma"

    # ------- Nombres de partners ------- #
    name_partner_ecuabet = "Ecuabet"
    name_partner_doradobet = "Doradobet"

    # ------- Nombres de paises ------- #
    name_pais_ecuador = "Ecuador"
    name_pais_nicaragua = "Nicaragua"
    name_pais_peru = "Perú"
    name_pais_el_salvador = "El Salvador"
    name_pais_costa_rica = "Costa Rica"

    # ------- Nombre de la plataforma ------- #
    name_plataforma = "Ad_Cash_Push_Ads_1"

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
    token = auth_response.json().get("token", "").strip()  # limpia espacios
    print("✅ Token obtenido correctamente")


    if not token:
        raise ValueError("❌ No se recibió token válido")


    # ------- Parametros y EndPoint para el reporte ------ #
    report_url = "https://api.myadcash.com/api/v1/advertiser-report"


    params = {
        "start_date": start_date,
        "end_date": end_date,
        "advertiser_id": "174198",
        "group_by": "date,country,campaignid,campaignname" # Se puede agrupar por maximo 4 parametros

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
    # print("🔎 Respuesta:", response.text)  # 👈 ver respuesta real

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

        print("✅ Datos recibidos correctamente desde la API")
        print(df_ad_cash.head())

    ################################################
    ####### Sección de diccionarios de mapeo #######
    ################################################

    # ------- Creación de la columna partner ------ #
    mapeo_partner = {

        # Ecuabet
        r'ecuab': name_partner_ecuabet,

        # Doradobet
        r'db|doradobet|_dorado': name_partner_doradobet
    }

    # ------- Creación de la columna País ------ #
    mapeo_paises = {

        # Ecuador
        r'ec' : name_pais_ecuador,

        # Nicaragua
        r'ni' : name_pais_nicaragua,

        # Perú
        r'pe' : name_pais_peru,

        # El salvador
        r'sv' : name_pais_el_salvador,

        # Costa rica
        r'cr' : name_pais_costa_rica
    }

    ###############################################
    ###### Fin seccion diccionarios de mapeo ######
    ###############################################

    # ------- Normalizar columna campaignname ------ #
    df_ad_cash["campaignname"] = df_ad_cash["campaignname"].str.lower().str.strip()

    # ------- Crear una columna partner y mapear valores de la columna campaignname ------ #
    df_ad_cash[name_column_partner] = (
        df_ad_cash["campaignname"]
        .apply(lambda x: next((v for k, v in mapeo_partner.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
    )

    # ------- Normalizar columna country ------ #
    df_ad_cash["country"] = df_ad_cash["country"].str.lower().str.strip()

    # ------- Crear una columna Pais y mapear valores de la columna country ------ #
    df_ad_cash[name_column_pais] = (
        df_ad_cash["country"]
        .apply(lambda x: next((v for k, v in mapeo_paises.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
    )

    # ------- Se crea una columna nueva con el nombre de la API ------- #
    df_ad_cash[name_column_plataforma] = name_plataforma

    # print("✅ Columna 'plataforma' creada correctamente")
    # print(df_ad_cash.head())

    # ------- Se renombran columnas ------ #
    df_ad_cash.rename(columns={
        "date": name_column_fecha,
        "spending": name_column_inversion
    }, inplace=True)

    # print("Nombres de columnas renombrados correctamente.")
    # print(df_ad_cash.head())

    # ------- Se crea el dataframe final solo con las columnas necesarias ------- #
    df_final_ad_cash = df_ad_cash[[name_column_fecha, name_column_partner, name_column_pais, name_column_inversion, name_column_plataforma]]

    # print("Dataframe final con las columnas necesarias.")
    # print(df_final_ad_cash.head())

    # ------- Se agrupa el DataFrame por fecha, partner y pais y se suma la columna inversión ------- #
    df_final_ad_cash = df_final_ad_cash.groupby([name_column_fecha, name_column_partner, name_column_pais, name_column_plataforma], as_index=False)[[name_column_inversion]].sum()

    print("Dataframe final con las columnas necesarias y agrupado.")
    print(df_final_ad_cash.head())

    # ------- Se guardan los resultados en un archivo CSV ------ #
    df_final_ad_cash.to_csv(name_csv_ad_cash, index=False, encoding="utf-8-sig")
    print(f"📁 Reporte guardado en '{name_csv_ad_cash.name}'")
    return df_final_ad_cash


    # # ------- Funcion para guardar en SQLite ------ #
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
    #     # Validar que el DataFrame no esté vacío
    #     if df.empty:
    #         print(f"\n ⚠️ El DataFrame está vacío. No se insertaron datos en la tabla '{nombre_tabla}'.\n ")
    #         return
    #     try:
    #         # Conexión a SQLite
    #         with sqlite3.connect(ruta_db) as conn:
    #             df.to_sql(nombre_tabla, conn, if_exists=if_exists, index=False)
    #         print(f"\n ✅ Se insertarón los datos con la tabla: '{nombre_tabla}' en la base de datos '{ruta_db.name}'.\n ")
        
    #     except Exception as e:
    #         print(f"\n ❌ Error al guardar en SQLite: {e}")

    # # ------- Se guarda el DataFrame en SQLite ------ #
    # guardar_en_sqlite(df_final_ad_cash, nombre_tabla_ad_cash, ruta_db, if_exists="replace")

