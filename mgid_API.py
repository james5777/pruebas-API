import requests
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import sqlite3
import re

def obtener_datos_mgid() -> pd.DataFrame:
    print("Iniciando proceso de obtencion de datos de la API de MGID...")

    # ------- Nombres de variables para rutas y nombres de tablas ------- #
    nombre_tabla_mgid = "general_mgid"
    ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
    name_csv_mgid = Path("Archivos/Archivos_csv/reporte_mgid.csv")

    # ------- Variables para nombres de columnas ------- #
    name_column_fecha = "Fecha"
    name_column_partner = "Partner"
    name_column_pais = "Pais"
    name_column_inversion = "Inversion"
    name_column_plataforma = "Plataforma"

    # ------- Nombres de partners ------- #
    name_partner_ecuabet = "Ecuabet"
    name_partner_aciertala = "Aciertala"

    # ------- Nombres de paises ------- #
    name_pais_ecuador = "Ecuador"
    name_pais_peru = "Perú"

    # ------- Nombre de la plataforma ------- #
    name_plataforma = "MGID_Nativo_1"

    # ------- Credenciales de acceso ------ #
    API_ID = "730589"  
    TOKEN = "06426fb424b53f2e9b3753a6694f7ef2"  

    # ------- EndPoint para informe granulado ------- #
    API_URL = f"https://api.mgid.com/v1/goodhits/clients/{API_ID}/statistics-reports"

    # ------- Headers y autorización ------- #
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    # ------- Parametros generales ------- #
    # ------- Rango de fechas, debe ser en el formato indicado, para que extraiga unicamente los datos en el rango ------- #
    date_from = "2025-10-01"
    date_to = "2025-10-14"

    # ------- Parametros de dimensiones y metricas ------- #
    dimensions = ["day", "campaignId", "campaignName"] ## Minimo 1, Maximo 3 (Se pueden cambiar revisando la documentacion de MGID) ##
    ### teaserId puede ser una dimension util ###
    metrics = [
        "spent", 
        "clicks", 
        "revenue",
        "profit", 
        "conversionsDecision", 
        "conversionsBuy" ## Minimo debe especificarse una metrica ##
    ]

    # ------- Parametros de fecha y limite de registros ------- #
    params = {
        "filters[dateRange][dateFrom]": date_from,
        "filters[dateRange][dateTo]": date_to,
        "limit": 50000  ## El maximo que devuelve la API son 50000 registros, si no se especifica el parametro limit, trae 20 registros por default.
    }

    # ------- Se formatean los dict de los parametros al formato que recibe la API mediante la URL ------- #
    for i, dim in enumerate(dimensions):
        params[f"dimensions[{i}]"] = dim
    for i, met in enumerate(metrics):
        params[f"metrics[{i}]"] = met

    # ------- Peticion a la API ------- #
    response = requests.get(API_URL, headers=headers, params=params)
    print("Código HTTP:", response.status_code)

    # ------- Validacion: si el status_code es diferente a 200, error ------- #
    if response.status_code != 200:
        print("❌ Error al obtener datos:")
        print(response.text)
        exit()

    # ------- Se almacena la respuesta en la variable Data ------- #
    data = response.json()

    # ------- Validacion: Si la key "data" no esta en la respuesta Json, error ------- #
    if "data" not in data or not data["data"]:
        print("⚠️ No se encontraron datos para el rango de fechas dado.")
        exit()

    # ------- Se convierten los valores de diccionarios anidados devueltos en texto plano facil de convertir a DataFrame, y los valores devueltos se guardan en la lista records ------- #
    records = []
    for item in data["data"]:
        row = {}
        for key, value in item.items():
            if isinstance(value, dict) and "amount" in value:
                row[key] = float(value["amount"])
            else:
                row[key] = value
        records.append(row)

    # ------- Se crea un dataframe y se ordena primero por fecha y luego por nombre campaña ------- #
    df_mgid = pd.DataFrame(records)
    df_mgid.sort_values(by=["day", "campaignName"], inplace=True, ignore_index=True)

    print("Datos recibidos desde la API.")
    print(df_mgid.head())

    ################################################
    ####### Sección de diccionarios de mapeo #######
    ################################################

    mapeo_partner = {

        # Ecuabet
        r'ecuab' : name_partner_ecuabet,

        # Aciertala
        r'aciert' : name_partner_aciertala
    }

    mapeo_paises = {

        # Ecuador
        r'ec_' : name_pais_ecuador,

        # Perú
        r'peru' : name_pais_peru
    }

    ###############################################
    ###### Fin seccion diccionarios de mapeo ######
    ###############################################

    # ------- Normalizar columna campaignName ------- #
    df_mgid["campaignName"] = df_mgid["campaignName"].str.lower().str.strip()

    # ------- Crear una columna partner y mapear valores de la columna campaignName ------- #
    df_mgid[name_column_partner] = (
        df_mgid["campaignName"]
        .apply(lambda x: next((v for k, v in mapeo_partner.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
    )

    # print("Columna partner creada correctamente.")
    # print(df_mgid.head())

    # ------- Crear una columna Pais y mapear valores de la columna campaignName ------- #
    df_mgid[name_column_pais] = (
        df_mgid["campaignName"]
        .apply(lambda x: next((v for k, v in mapeo_paises.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
    )

    # print("Columna Pais creada correctaamente.")
    # print(df_mgid.head())

    # ------- Se crea una nueva columna con el nombre de la API ------- #
    df_mgid[name_column_plataforma] = name_plataforma

    # print("Columna plataforma creada correctamente")
    # print(df_mgid.head())

    # ------- Se renombran columnas ------- #
    df_mgid.rename(columns={
        "day" : name_column_fecha,
        "spent" : name_column_inversion
    }, inplace=True)

    # print("Nombres de columnas renombrados correctamente.")
    # print(df_mgid.head())

    # ------- Se crea el DataFrame final solo con las columnas necesarias ------- #
    df_final_mgid = df_mgid[[name_column_fecha, name_column_partner, name_column_pais,name_column_inversion, name_column_plataforma]]

    # print("DataFrame final con las columnas necesarias.")
    # print(df_final_mgid.head())

    # ------- Se agrupa el DataFrame por fecha, partner y pais y se suma la columna inversion ------- #
    df_final_mgid = df_final_mgid.groupby([name_column_fecha, name_column_partner, name_column_pais, name_column_plataforma], as_index=False)[[name_column_inversion]].sum()

    print("DataFrame final con las columnas necesarias y agrupado.")
    print(df_final_mgid.head())

    # ------- Se guardan los resultados en un archivo CSV ------- #
    df_final_mgid.to_csv(name_csv_mgid, index=False, encoding="utf-8-sig")
    print(f"📁 Reporte guardado en '{name_csv_mgid.name}'")
    return df_final_mgid

    # # ------- Funcion para guardar en SQLite ------- #
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

    # # ------- Se guarda el dataframe en SQLite ------- #
    # guardar_en_sqlite(df_mgid, nombre_tabla_mgid, ruta_db, if_exists="replace")

