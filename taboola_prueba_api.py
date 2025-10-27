import requests
import pandas as pd
import sqlite3

# -------- 🔐 CREDENCIALES DE ACCESO -------- #
ACCOUNT_ID = "quotamediasam-doradobetcostarica-sc"   # Ejemplo: "my-advertiser"
ACCESS_TOKEN = "CRQ1AAAAAAAAEdKwmAAAAAAAGAEgAClo3cMXmgEAADooYTdlOTkwNmJhMDBhM2E2NWY1NWFmNzJkZGI4OTNiMDgxYzgzOWUyMUAC::fdd7a4::a17564"

# -------- 🌐 ENDPOINT DEL REPORTE -------- #
API_URL = f"https://backstage.taboola.com/backstage/api/1.0/{ACCOUNT_ID}/reports/campaign-summary/dimensions/campaign_breakdown"

# -------- 🧭 RANGO DE FECHAS -------- #
start_date = "2025-10-10"
end_date = "2025-10-21"

# -------- 📦 PARÁMETROS DEL REPORTE -------- #
params = {
    "start_date": start_date,
    "end_date": end_date,
    "limit": 5000,             # puedes ajustar este número
    "include_paid_traffic": "true",
    "group_by": "date",
    "dimensions" : ["day"]
}

# -------- 🧾 HEADERS -------- #
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

# -------- 🚀 SOLICITUD A LA API -------- #
print("🔄 Consultando estadísticas de Taboola...")
response = requests.get(API_URL, headers=headers, params=params)
print("Código HTTP:", response.status_code)
print(response.json())

# -------- 📊 PROCESAR RESPUESTA -------- #
# if response.status_code == 200:
#     data = response.json()
    
#     if "results" in data and len(data["results"]) > 0:
#         df_taboola = pd.DataFrame(data["results"])
        
#         # Ordenar por fecha y campaña
#         df_taboola.sort_values(by=["date", "campaign"], inplace=True, ignore_index=True)
        
#         # Mostrar primeras filas
#         print("\n✅ Primeros registros obtenidos:")
#         print(df_taboola.head())

#         # Guardar CSV
#         df_taboola.to_csv("taboola_reporte.csv", index=False, encoding="utf-8-sig")
#         print("\n📁 Reporte guardado como 'taboola_reporte.csv'")
#     else:
#         print("⚠️ No se encontraron datos en el rango de fechas.")
# else:
#     print("❌ Error al consultar la API:", response.text)
