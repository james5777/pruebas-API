import requests
import datetime
import pandas as pd
from pathlib import Path
import sqlite3
import re

# ------- Token de acceso y de refresco ------- #
id_token = "eyJraWQiOiJsMDdheTRNdEhWTWEwTDdvZEVReUorNUg1OHI1R2syaU1lK0dORTNCenV3PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoieXl2NmQyN3ZoemVnRS0zbVZHd0FydyIsInN1YiI6IjRiZTZjODhlLWI1NWUtNDU5YS1hY2IxLWY1NWIxYzY3MDE4ZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9XNWF4YWFxMWwiLCJjb2duaXRvOnVzZXJuYW1lIjoiNGJlNmM4OGUtYjU1ZS00NTlhLWFjYjEtZjU1YjFjNjcwMThkIiwib3JpZ2luX2p0aSI6IjllMTYyM2RiLWMzNzMtNGQwYi1iNmM1LWUzNTc1NGVjZmNhYiIsImF1ZCI6IjF0YzM3aTVvaWhucjA0YmNpcTMzMzBkbHRvIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NjI4NjgxOTEsIm5hbWUiOiJUaGVvZG9ybyIsImV4cCI6MTc2Mjk1NDU5MSwiaWF0IjoxNzYyODY4MTkxLCJmYW1pbHlfbmFtZSI6IkRpa3V5YW1hIiwianRpIjoiODk1NDQ5MDItOTA4Yy00OWZhLWFmMGUtYWMzZjdiOWZjMDkxIiwiZW1haWwiOiJ0aGVvZG9yby5kaWt1eWFtYUBxdW90YW1lZGlhLmNvIn0.uQ4akozwJmyiskZ9tTX9opGARaEXWbKQEqhKEH26T4XwZIgVRhQWWxFeBLUHe31lk6B3OKLDOJP38Sk4vaWrS8daJMwaDm6ReeotOSW3gJeiwWYmNmUD40Ye4zpe5dAfUeXiuyn_bzCDMieSPb6YB9SnKILedBSzQ113JtSHYB2qHPXwnkN1eX7TbI5tyoHxRKi6YqspsKRw017mwSP3pLPjX0wWwk5V3ZmjdUHXhTxHktYSOz9dUs1tB7Afirpp2mwOFYp5xOkRfZmWu5gCFHzwndF7mSVIQ4pElznGZVYWzEtEkqTnsCyfz40VPtUZ5IjvF7crZP0EPhy6yTYQVg"  # token actual
refresh_token = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.mYWlxCA9fA6oloRic042N-FB1gmW92tnPYuUk3r-tjLWnxrao2QTFd0YSxI-Dp80CzDxFxewzyzdnP_EzBe954gdJc-rZKJt3nZmxUNtGBw2UfLKHALJOOAyIlcqzOgwj94jCTQS19VOTs3h1FxBmV0q4r9TUuVqqqfDpxUfOTs96DZKhFLfHYmJkR0_w-UUyWy55e4C7XFe6c-kqePOjDU9HwSswQATIy0pKMCiSxaUPx69kdWXubWgryJnCuv_KQ6iDGP3rt-PIjhnamOWpL86X9bieCUgzazmPyqqMd3tO0fSQixGJjgeH3yEovU0J4IfcJ1fp1tAPOheT93hrw.DyzO8tsMh-Hmvjys.sOI6NxgadKr2xOmN8zfAtShAgYLkiHGtpTagUT8Nlvbo7craseYyatNHMrc9V2kf7EUL8J4E8YJc-6GGAeY7tT0e3reW26QwFZjAbGwBfk3CId3qN_FvGBRhaxa20epGcq7OmpdOVLNJCziUwIKbyVzTnYaOGGJKp-lvU2CViw9E4PncXOk_z2WapBjjkeY0_-WmdvKKsWMHxyw5skFITOGWOCBYWBovESX2j6lnhB8tS8iOnj0lqT2fHtQPajjk7OFpAtBAr_9qMjqOyUlj18_-U5AEVxRsxYeREp_LiXfHaRQjy8HM5mfQrHoqkALj6QIAzDxuMuAJiaMFyu84_Xa_X-3D2QxRQEM3GxJkGZiu2r8J50g16YsXwvr_ci5l-kUBhm4q936JmSQpuiHwuPfYAvrRdFOczPmkfFRzz0nCTzpIEoIb1syP6a_uhEpZBSkTsED1y-XGsAM0zfIFYcuN0Hp1MMrZUTIP-pyKYJg7KHAcE539TxGcXGkDKei67E68yxmyPPFOsZ_bs8TM9LPgSkz973L5QEQqKEVAlqLmgplNYduvB9RNO2um4wxu7HkytjIo7hXt3najpzAF4jnxipouuN4xovJ60yNrLN_Yp3QlxGneq2ET2vLmjgPdGbrYdfqfYBM9xjccZtEGyAokmsMqum6B6tRE2v36pb_kt9vDTwo2Efaridq_EJVfKaBzVR9FWoMIvM44vI7PgGVg2kYjOAbBvVatdJS1Kweb4F2u3SVP_c6MfIdNqpZ-1YCIfllDiq3oEeqOlzvGWazPBvsDgGQnbp-MF_d6n6LFE3XcsF4XfqhcE2N5R-sod35vfKL-3ggKEAGrLVFWn7OaUo1jBOF-xKKmIhmEH73LVdnZ4ACOlwGesNzj47JYnf3o64KQj8xNFfg0TEGaAXu5Cyf8-Exo8jf4rkzNz4uDKArHSgvL4bo28aY66B-5i-UaVKkkVW89OwM50SwqGyqUsSqi_YtMIIzz52uPwcMDt_PXXsIOMuwMptF_gcpnLZS9L96MglDCCl-hS233ZNqYRgv0-n07zP9iGVsCevPgmXysOdaVfjdaENmgrX6tTxbnQ3JuS-kXUPxteGQ_4f4VxoBC3B_q9dOIGVpukvEDY7YYMfJV4-XLZtHThyu1-6zRWqb50RO_Lyt9VFcg_rw8u1cn1I4HJJ6L4b1WnxsFZp63zjyPsFzcZ9aUmdUETBGK5ChrlgKfdjVwsPR4pEg566QV9wnf5QnTI-lsAW9coM_R4c50POj0emucMKA1Z0Y.B6h-WjsjxSj0YWqQzbxBew"  # lo que te da el sistema al generar el token

def obtener_datos_sportradar() -> pd.DataFrame:
    print("Iniciando proceso de obtencion de datos de la API de SportRadar...")

    # ------- Parametros editables ------- #
    start_date = "2025-10-01"
    end_date = "2025-10-14"

    # ------- Nombres de variables para rutas y nombres de tablas ------- #
    nombre_tabla_sportradar = "general_sportradar"
    ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
    name_csv_sportradar = Path("Archivos/Archivos_csv/reporte_sportradar.csv")

    # ------- Variables para nombres de columnas ------- #
    name_column_fecha = "Fecha"
    name_column_partner = "Partner"
    name_column_pais = "Pais"
    name_column_inversion = "Inversion"
    name_column_registros = "Registros"
    name_column_primeros_depositos = "primeros_Depositos"

    # ------- Nombres de Partners ------- #
    name_partner_doradobet = "Doradobet"
    name_partner_ecuabet = "Ecuabet"
    name_partner_ganaplay = "GanaPlay"
    name_partner_paniplay = "Paniplay"

    # ------- Nombres de paises ------- #
    name_pais_chile = "Chile"
    name_pais_costa_rica = "Costa Rica"
    name_pais_ecuador = "Ecuador"
    name_pais_guatemala = "Guatemala"
    name_pais_honduras = "Honduras"
    name_pais_peru = "Perú"
    name_pais_el_salvador = "El Salvador"

    
    # token_expiration = datetime.datetime.now() + datetime.timedelta(hours=6)

    # ------- Funcion que usa el token de refresco para actualizar el token ------- #
    def refresh_id_token():
        global id_token
        url = "https://api.api-access.iam.ads.sportradar.com/prod/oauth2/token"
        headers = {"Authorization": f"Bearer {id_token}"}
        body = {"refreshToken": refresh_token}
        response = requests.post(url, json=body, headers=headers)

        if response.status_code == 200:
            new_data = response.json()
            id_token = new_data["idToken"]  # nuevo token
            # token_expiration = datetime.datetime.now() + datetime.timedelta(hours=6)
            print("✅ Token actualizado correctamente")
        else:
            print("❌ Error al renovar token:", response.text)

    # ------- Funcion para verificar si ya pasaron 6 horas desde la ultima vez que se ejecuto el token ------- #
    def get_data_from_api():
        # if datetime.datetime.now() >= token_expiration:
        #     refresh_id_token()

        print("Verificando y renovando token de acceso...")
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

    # if datetime.datetime.now() >= token_expiration:
    refresh_id_token()

    # ------- Peticion a la API ------- #
    response = requests.post(url, json=body, headers=headers)
    data = response.json()
    print("Codigo de estado HTTP")
    print(response.status_code)

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
    print("Dataframe inicial recibido desde la API.")
    print(df_sportradar.head())

    ################################################
    ####### Sección de diccionarios de mapeo #######
    ################################################

    mapeo_partner = {

        # Doradobet
        r'1251' : name_partner_doradobet,

        # Ecuabet
        r'1252' : name_partner_ecuabet,

        # Ganaplay
        r'3151' : name_partner_ganaplay,

        # Paniplay
        r'1847' : name_partner_paniplay
    }

    mapeo_paises = {
        
        # Chile
        r'cl' : name_pais_chile,

        # Costa rica
        r'cr' : name_pais_costa_rica,

        # Ecuador
        r'ec' : name_pais_ecuador,

        # Guatemala
        r'gt' : name_pais_guatemala,

        # Honduras
        r'hn' : name_pais_honduras,

        # Perú
        r'pe' : name_pais_peru,

        # El salvador
        r'sv' : name_pais_el_salvador
    }

    ###############################################
    ###### Fin seccion diccionarios de mapeo ######
    ###############################################

    # ------- Crear una columna partner y mapear valores de la columna advertiser_id ------ #
    df_sportradar[name_column_partner] = (
        df_sportradar["advertiser_id"]
        .apply(lambda x: next((v for k, v in mapeo_partner.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
    )

    # print("Dataframe con columna partner creada.")
    # print(df_sportradar.head())

    # ------- Normalizar columna country ------- #
    df_sportradar["country"] = df_sportradar["country"].str.lower().str.strip()

    # ------- Crear una columna Pais y mapear valores de la columna country ------- #
    df_sportradar[name_column_pais] = (
        df_sportradar["country"]
        .apply(lambda x: next((v for k, v in mapeo_paises.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
    )

    # print("Dataframe con columna Pais creada.")
    # print(df_sportradar.head())

    # ------- Se renombran las columnas necesarias ------- #
    df_sportradar.rename(columns={
        "day" : name_column_fecha,
        "pixel.type.reg_finished" : name_column_registros,
        "pixel.type.ftd" : name_column_primeros_depositos,
        "payout.actual_adv_usd" : name_column_inversion
    }, inplace=True)

    # print("Dataframe con columnas renombradas.")
    # print(df_sportradar.head())

    # ------- Se crea un nuevo DataFrame solo con las columnas necesarias ------- #
    df_final_sportradar = df_sportradar[[name_column_fecha, name_column_partner, name_column_pais, name_column_registros, name_column_primeros_depositos, name_column_inversion]]

    # print("Dataframe final con las columnas necesarias.")
    # print(df_final_sportradar.head())

    # ------- Se agrupa el DataFrame por fecha, partner y pais y se suman las columnas de registros, ftds e inversión ------- #
    df_final_sportradar = df_final_sportradar.groupby([name_column_fecha, name_column_partner, name_column_pais], as_index=False)[[name_column_registros,name_column_primeros_depositos,name_column_inversion]].sum()

    print("DataFrame final con las columnas necesarias y agrupado")
    print(df_final_sportradar.head())

    # # ------- Se calculan metricas adicionales ------- #
    # if not df_sportradar.empty:
    #     df_sportradar["CPL"] = (df_sportradar["payout.actual_adv_usd"] / df_sportradar["pixel.type.reg_finished"]).round(2)
    #     df_sportradar["CPA"] = (df_sportradar["payout.actual_adv_usd"] / df_sportradar["pixel.type.ftd"]).round(2)
    # else:
    #     print("⚠️ No se encontraron registros en el rango de fechas.")

    # === 7️⃣ Guardar resultados ===
    df_final_sportradar.to_csv(name_csv_sportradar, index=False, encoding="utf-8-sig")
    print("✅ Datos guardados en 'reporte_sportradar.csv'")
    return df_final_sportradar

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

    # guardar_en_sqlite(df_sportradar, nombre_tabla_sportradar, ruta_db, if_exists="replace")



