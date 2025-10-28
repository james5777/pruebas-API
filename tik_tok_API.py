import requests
import time
import pandas as pd
from io import StringIO

# === ⚙️ CONFIGURACIÓN ===
ACCESS_TOKEN = "d4f9ec23c728b52cbc9a7a1dbdc3cc4321608510"        # ⚠️ Cambia por tu token real
ADVERTISER_ID = "7451865507243753473"      # ⚠️ Cambia por tu ID real
START_DATE = "2025-10-01"
END_DATE = "2025-10-14"
OUTPUT_FILE = "tiktok_report.csv"

# === 📊 PASO 1: Crear tarea de reporte asincrónico ===
url_create = "https://business-api.tiktok.com/open_api/v1.3/report/task/create/"

payload = {
    "advertiser_id": ADVERTISER_ID,
    "report_type": "BASIC",
    "data_level": "AUCTION_CAMPAIGN",
    "dimensions": ["stat_time_day", "campaign_id", "campaign_name", "country_code"],
    "metrics": ["spend", "impressions", "clicks", "cpc", "ctr", "cpm", "conversions"],
    "start_date": START_DATE,
    "end_date": END_DATE,
    "output_format": "CSV_DOWNLOAD",
    "file_name": "tiktok_daily_report"
}

headers = {
    "Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

print("🌀 Creando tarea de reporte en TikTok...")
response = requests.post(url_create, json=payload, headers=headers)
print("Código HTTP:", response.status_code)

if response.status_code != 200:
    print("❌ Error al crear el reporte:", response.text)
    exit()

task_data = response.json()
print("Respuesta:", task_data)

if task_data.get("code") != 0:
    print("❌ Error al crear el reporte:", task_data)
    exit()

task_id = task_data["data"]["task_id"]
print(f"✅ Tarea creada con ID: {task_id}")

# === ⏳ PASO 2: Revisar estado de la tarea ===
url_check = "https://business-api.tiktok.com/open_api/v1.3/report/task/check/"
status = "PROCESSING"

while status == "PROCESSING":
    print("⏳ Revisando estado...")
    check_payload = {"task_id": task_id}
    resp_check = requests.get(url_check, params=check_payload, headers=headers)
    data_check = resp_check.json()
    status = data_check.get("data", {}).get("status", "UNKNOWN")
    print(f"Estado: {status}")
    if status == "SUCCESS":
        break
    elif status == "FAIL":
        print("❌ Error: la tarea falló.")
        exit()
    time.sleep(10)

# === 📥 PASO 3: Descargar reporte ===
url_download = "https://business-api.tiktok.com/open_api/v1.3/report/task/download/"
download_payload = {"task_id": task_id}

print("📥 Descargando reporte...")
resp_download = requests.get(url_download, params=download_payload, headers=headers)
download_data = resp_download.json()

if download_data.get("code") != 0:
    print("❌ Error al obtener enlace de descarga:", download_data)
    exit()

download_url = download_data["data"]["url"]
print(f"✅ URL de descarga lista:\n{download_url}")

# === 📄 PASO 4: Descargar archivo CSV ===
csv_response = requests.get(download_url)
df = pd.read_csv(StringIO(csv_response.text))

print("\n✅ Reporte descargado y convertido a DataFrame:")
print(df.head())

# Guardar a archivo local
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n💾 Archivo guardado como {OUTPUT_FILE}")
