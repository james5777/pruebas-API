import requests
import pandas as pd
from pathlib import Path
import sqlite3
import re

print("Iniciando proceso de obtencion de datos de la API de Taboola...")

# ------- Parametros editables ------- #
start_date = "2025-10-01"
end_date = "2025-10-14"

# ------- Nombres de variables para rutas y nombres de tablas ------- #
nombre_tabla_taboola = "general_taboola"
ruta_db = Path("Archivos/Archivo_base_de_datos/base_de_datos_api")
name_csv_taboola = Path("Archivos/Archivos_csv/reporte_taboola.csv")

# ------- Variables para nombres de columnas ------- #
name_column_fecha = "Fecha"
name_column_partner = "Partner"
name_column_pais = "Pais"
name_column_inversion = "Inversion"

# ------- Nombres de partners ------- #
name_partner_doradobet = "Doradobet"

# ------- Nombres de paises ------- #
name_pais_costa_rica = "Costa Rica"

# ------- Funcion para obtener token y acceso ------- #
def get_access_token():
    url = "https://backstage.taboola.com/backstage/oauth/token"
    payload = {
        "client_id": "0d90885f1a9e4313ac03b6e004143c08",
        "client_secret": "00bd96b8478c4e5b84eda0d464e4cb3f",
        "grant_type": "client_credentials"
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    else:
        raise Exception(f"Error al obtener token: {response.text}")


# ------- Se asigna el token de acceso a la variable ------- #
access_token = get_access_token()

# ------- Se crea un diccionario con los nombres de los partner-pais y el id_Advertiser ------- #
advertisers = {
    "Doradobet - CL": "doradobetchile",
    "Doradobet - EC": "doradobetecuador",
    "Doradobet - CR": "quotamediasam-doradobetcostarica-sc",
    "Ecuabet": "quotamediasam-ecuabet-sc"
}

# ------- Se hace la llamada a la API por cada uno de los advertiser y se guarda en la lista "All_data" ------- #
all_data = []

for advertiser_name, account_id in advertisers.items():
    print(f"📊 Descargando datos de: {advertiser_name}...")

    url = f"https://backstage.taboola.com/backstage/api/1.0/{account_id}/reports/campaign-summary/dimensions/campaign_day_breakdown"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "metrics": "impressions,clicks,spent,ctr,cpc,currency",
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    print("Codigo de estado HTTP")
    print(response.status_code)

    if response.status_code == 200:
        data = response.json().get("results", [])
        df = pd.DataFrame(data)
        if not df.empty:
            df["advertiser"] = advertiser_name  # 👈 Agregar columna con el nombre del anunciante
            all_data.append(df)
        print(f"✅ Datos obtenidos de {advertiser_name}")
    else:
        print(f"❌ Error con {advertiser_name}: {response.status_code} - {response.text}")

# ------- Crear un DataFrame general de todos los datos de todos los advertiser ------- #
if all_data:
    df_taboola = pd.concat(all_data, ignore_index=True)
    print("\n✅ Reporte combinado listo:")
else:
    print("⚠️ No se obtuvieron datos de ningún anunciante.")

# ------- Se ordena el dataframe por fecha y luego por partner ------- #
df_taboola.sort_values(by=["date", "advertiser"], inplace=True, ignore_index=True)

# ------- Normalizacion de columna date ------- #
df_taboola["date"] = pd.to_datetime(df_taboola["date"]).dt.strftime("%Y-%m-%d")

print("Dataframe inicial recibido desde la API")
print(df_taboola.head())

################################################
####### Sección de diccionarios de mapeo #######
################################################

mapeo_partner = {

    # Doradobet
    r'doradob' : name_partner_doradobet
}

mapeo_paises = {

    # Costa rica
    r'cr_' : name_pais_costa_rica
}

###############################################
###### Fin seccion diccionarios de mapeo ######
###############################################

# ------- Normalizar columna campaign_name ------- #
df_taboola["campaign_name"] = df_taboola["campaign_name"].str.lower().str.strip()

# ------- Crear una columna partner y mapear valores de la columna campaign_name ------- #
df_taboola[name_column_partner] = (
    df_taboola["campaign_name"]
    .apply(lambda x: next((v for k, v in mapeo_partner.items() if pd.notna(x) and re.search(k,x)), "Desconocido"))
)

# print("Columna partner creada correctamente")
# print(df_taboola.head())

# ------- Crear columna pais y mapear valores de la columna campaign_name ------- #
df_taboola[name_column_pais] = (
    df_taboola["campaign_name"]
    .apply(lambda x: next((v for k, v in mapeo_paises.items() if pd.notna(x) and re.search(k, x)), "Desconocido"))
)

# print("Columna Pais creada correctamente")
# print(df_taboola.head())

# ------- Se renombran columnas ------- #
df_taboola.rename(columns={
    "date" : name_column_fecha,
    "spent" : name_column_inversion
}, inplace=True)

# print("Nombres de columnas renombrados correctamente.")
# print(df_taboola.head())

df_final_taboola = df_taboola[[name_column_fecha, name_column_partner, name_column_pais, name_column_inversion]]

# print("DataFrame final con las columnas necesarias.")
# print(df_final_taboola.head())

# ------- Se agrupa el DataFrame por fecha, partner y pais y se suma la columna inversion ------- #
df_final_taboola = df_final_taboola.groupby([name_column_fecha, name_column_partner, name_column_pais], as_index=False)[[name_column_inversion]].sum()

print("DataFrame final con las columnas necesarias y agrupado.")
print(df_final_taboola.head())

# ------- Se convierte el dataframe a CSV ------- #
df_final_taboola.to_csv(name_csv_taboola, index=False, encoding="utf-8-sig")

# # # ------- Se crea la funcion de guardar en SQLite------- #
# # def guardar_en_sqlite(df: pd.DataFrame, nombre_tabla: str, ruta_db: Path, if_exists: str = "replace") -> None:

# #     """
# #     Guarda un DataFrame en una base de datos SQLite, creando o actualizando la tabla según se especifique.

# #     Parámetros:
# #     ----------
# #     df : pd.DataFrame
# #         El DataFrame que se desea guardar en la base de datos.
    
# #     nombre_tabla : str
# #         El nombre de la tabla en la base de datos SQLite.
    
# #     ruta_db : Path
# #         Ruta al archivo `.sqlite` o `.db` donde se guardarán los datos.
    
# #     if_exists : str, opcional
# #         Comportamiento si la tabla ya existe. Valores permitidos:
# #         - 'replace' (por defecto): elimina la tabla y la vuelve a crear.
# #         - 'append': agrega los datos sin eliminar la tabla.
# #         - 'fail': lanza una excepción si la tabla ya existe.

# #     Retorna:
# #     -------
# #     None
# #         Esta función no retorna un valor. Inserta los datos directamente en la base de datos.
# #     """
# #     # Validar que el Dataframe no esté vacío
# #     if df.empty:
# #         print(f"\n ⚠️ El dataframe está vacío. No se insertaron datos en la tabla '{nombre_tabla}'.\n ")
# #         return
# #     try:
# #         # Conexion con SQLite
# #         with sqlite3.connect(ruta_db) as conn:
# #             df.to_sql(nombre_tabla, conn, if_exists=if_exists, index=False)
# #         print(f"\n ✅ Se insertaron los datos en la tabla: '{nombre_tabla}' en la base de datos '{ruta_db.name}'.\n ")
    
# #     except Exception as e:
# #         print(f"\n ❌ Error al guardar en SQLite: {e}")

# # # ------- Se guarda el DataFrame en SQLite ------- #
# # guardar_en_sqlite(df_taboola, nombre_tabla_taboola, ruta_db, if_exists="replace")