import pandas as pd
from pathlib import Path
import adcash_API as ac
import sportradar_API as sr
import mgid_API as mg
import propellerads_API as pa
import taboola_API as tb
import tik_tok_API as tt


# ------- Nombres de variables para rutas y nombres de tablas ------- #
name_csv_general = Path("Archivos/Archivos_csv/reporte_general.csv")

# Obtener datos de Ad Cash
df_ad_cash = ac.obtener_datos_ad_cash()

# Obtener datos de Sportradar
df_sportradar = sr.obtener_datos_sportradar()

# Obtener datos de MGID
df_mgid = mg.obtener_datos_mgid()

# Obtener datos de PropellerAds
df_propellerads = pa.obtener_datos_propellerads()

# Obtener datos de Taboola
df_taboola = tb.obtener_datos_taboola()

# Obtener datos de TikTok
df_tiktok = tt.obtener_datos_tiktok()

# ------- Concateno todos los Dataframes ------- #
df_todos = pd.concat([df_ad_cash, df_sportradar, df_mgid, df_propellerads, df_taboola, df_tiktok], ignore_index=True)

print("✅ Datos de todas las plataformas obtenidos correctamente")
print(df_todos.head())

df_todos.to_csv(name_csv_general, index=False, encoding="utf-8-sig")
print(f"📁 Reporte guardado en '{name_csv_general}'")
