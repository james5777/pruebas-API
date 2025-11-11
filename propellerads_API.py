import requests
import pandas as pd
import json
import sqlite3
from pathlib import Path
import re

def obtener_datos_propellerads() -> pd.DataFrame:
    print("Iniciando proceso de obtencion de datos de la API de PropellerAds...")

    # ------- Nombres de variables para rutas y nombres de tablas ------- #
    nombre_tabla_propellerads = "general_propellerads"
    ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
    name_csv_propellerads = Path("Archivos/Archivos_csv/reporte_propellerads.csv")

    # ------- Variables para nombres de columnas ------- #
    name_column_fecha = "Fecha"
    name_column_partner = "Partner"
    name_column_pais = "Pais"
    name_column_inversion = "Inversion"
    name_column_plataforma = "Plataforma"

    # ------- Nombres de partners ------- #
    name_partner_doradobet = "Doradobet"
    name_partner_aciertala = "Aciertala"
    name_partner_ecuabet = "Ecuabet"
    name_partner_paniplay = "Paniplay"
    name_partner_camanbet =  "Camanbet"

    # -------- Nombre de paises ------- #
    name_pais_chile = "Chile"
    name_pais_costa_rica = "Costa Rica"
    name_pais_ecuador = "Ecuador"
    name_pais_guatemala = "Guatemala"
    name_pais_peru = "Perú"
    name_pais_el_salvador = "El Salvador"
    name_pais_honduras = "Honduras"
    name_pais_nicaragua = "Nicaragua"
    name_pais_venezuela = "Venezuela"

    # ------- Nombre de la plataforma ------- #
    name_plataforma = "Propellerads_Push_Ads_4"

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

        else:
            print("No se encontraron datos en el rango de fecha especificado")
    else:
        print("Error al consultar la API ❌")
        print(response.text)

    # ------- Mostrar data obtenida desde la API ------- #
    print("Datos recibidos correctamente desde la API")
    print(df_propellerads.head())

    ################################################
    ####### Sección de diccionarios de mapeo #######
    ################################################

    # ------- Creacion de la columna partner ------- #
    mapeo_partner = {
        
        # Doradobet
        r'dorad' : name_partner_doradobet,

        # Aciertala
        r'_aciert|_aciert' : name_partner_aciertala,

        # Ecuabet
        r'ecuab' : name_partner_ecuabet,

        # Paniplay
        r'panip' : name_partner_paniplay,

        # Camanbet
        r'camanb' : name_partner_camanbet
    }

    # ------- Creacion de la columna Pais ------- #
    mapeo_paises = {

        # Chile
        r'ch_' : name_pais_chile,

        # Costa rica
        r'cr_' : name_pais_costa_rica,

        # Ecuador
        r'ec_' : name_pais_ecuador,

        # Guatemala
        r'gt_' : name_pais_guatemala,

        # Perú
        r'pe_' : name_pais_peru,

        # El salvador
        r'es_' : name_pais_el_salvador,

        # Honduras
        r'hn_' : name_pais_honduras,

        # Nicaragua
        r'nc_' : name_pais_nicaragua,

        # Venezuela
        r'vz_' : name_pais_venezuela
    }
    ###############################################
    ###### Fin seccion diccionarios de mapeo ######
    ###############################################

    # ------- Normalizar columna campaign_name ------- #
    df_propellerads["campaign_name"] = df_propellerads["campaign_name"].str.lower().str.strip()

    # ------- Crear columna partner y mapear valores de la columna campaign_name ------- #
    df_propellerads[name_column_partner] = (
        df_propellerads["campaign_name"]
        .apply(lambda x: next((v for k, v in mapeo_partner.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
    )

    # print("Dataframe con la columna partner creada.")
    # print(df_propellerads.head())

    # ------- Crear columna Pais y mapear valores de la columna campaign_name ------- #
    df_propellerads[name_column_pais] = (
        df_propellerads["campaign_name"]
        .apply(lambda x: next((v for k, v in mapeo_paises.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
    )

    # print("Columna Pais creada correctamente")
    # print(df_propellerads.head())

    # ------- Se crea ima columna nueva con el nombre de la API ------- #
    df_propellerads[name_column_plataforma] = name_plataforma

    # print("Columna plataforma creada correctamente.")
    # print(df_propellerads.head())

    # ------- Se renombran columnas ------- #
    df_propellerads.rename(columns={
        "date_time" : name_column_fecha,
        "spent" : name_column_inversion
    }, inplace=True)

    # ------- Se crea el dataframe final solo con las columnas necesarias ------- #
    df_final_propellerads = df_propellerads[[name_column_fecha, name_column_partner, name_column_pais, name_column_inversion, name_column_plataforma]]

    # print("Dataframe final solo con las columnas necesarias.")
    # print(df_final_propellerads.head())

    # ------- Se agrupa el DataFrame por fecha, partner y pais, y se suma la columna inversion ------- #
    df_final_propellerads = df_final_propellerads.groupby([name_column_fecha, name_column_partner, name_column_pais, name_column_plataforma], as_index=False)[[name_column_inversion]].sum()

    print("Dataframe final con las columnas necesarias y agrupado")
    print(df_final_propellerads.head())

    # -------- Convierto el dataframe a CSV ------- #
    df_final_propellerads.to_csv(name_csv_propellerads, index=False, encoding="utf-8-sig")
    print(f"📁 Reporte guardado en '{name_csv_propellerads.name}'")
    return df_final_propellerads

    # # -------- Funcion para guardar en SQLite ------- #    
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
    #     # Validar que el DataFrame esté vacío.
    #     if df.empty:
    #         print(f"\n ⚠️ El DataFrame está vacío. No se insertaron datos en la tabla '{nombre_tabla}'.\n ")
    #         return
    #     try:
    #         # Conexión a SQLite
    #         with sqlite3.connect(ruta_db) as conn:
    #             df.to_sql(nombre_tabla, conn, if_exists=if_exists, index=False)
    #         print(f"\n ✅ Se insertaron los datos con la tabla '{nombre_tabla}' en la base de datos '{ruta_db.name}'.\n ")
        
    #     except Exception as e:
    #         print(f"\n ❌ Error al guardar en SQLite: {e}")

    # # -------- Se guarda el DataFrame en SQLite ------- #
    # guardar_en_sqlite(df_propellerads, nombre_tabla_propellerads, ruta_db, if_exists="replace")


