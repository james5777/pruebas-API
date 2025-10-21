import requests
import json
import pandas as pd

# === CONFIGURACIÓN GENERAL ===
api_id = "730589"
api_token = "06426fb424b53f2e9b3753a6694f7ef2"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}

startdate = "2025-10-01"
enddate = "2025-10-10"

def obtener_estadisticas(api_id):
    # --- 1️⃣ Obtener lista de campañas (nombre y país)
    url_campaigns = f"https://api.mgid.com/v1/goodhits/clients/{api_id}/campaigns"
    response_campaigns = requests.get(url_campaigns, headers=headers)

    if response_campaigns.status_code != 200:
        print("❌ Error al obtener campañas:", response_campaigns.text)
        return None

    campaigns_data = response_campaigns.json()
    campaigns_info = {}

    # Guardamos nombre y país de cada campaña
    for camp in campaigns_data.get("data", []):
        campaigns_info[str(camp.get("id"))] = {
            "name": camp.get("name", "Sin nombre"),
            "country": camp.get("geo", "Desconocido"),
        }

    # --- 2️⃣ Obtener estadísticas por campaña
    url_stats = f"https://api.mgid.com/v1/goodhits/clients/{api_id}/campaigns-stat"
    params = {"dateInterval": "interval",
                "startDate": startdate,
                "endDate": enddate
        }

    response_stats = requests.get(url_stats, headers=headers, params=params)
    print("Código de estado HTTP:", response_stats.status_code)

    if response_stats.status_code != 200:
        print("❌ Error al obtener estadísticas:", response_stats.text)
        return None

    stats_data = response_stats.json()

    if "campaigns-stat" not in stats_data:
        print("⚠️ Estructura inesperada de respuesta")
        print(json.dumps(stats_data, indent=2, ensure_ascii=False))
        return None

    campaigns_stats = stats_data["campaigns-stat"]

    registros = []
    for campaign_id, stats in campaigns_stats.items():
        info = campaigns_info.get(str(campaign_id), {})
        registros.append({
            "ID Campaña": campaign_id,
            # "Nombre Campaña": info.get("name", "Desconocida"),
            # "País": info.get("country", "Desconocido"),
            "Impresiones": stats.get("imps", 0),
            "Clicks": stats.get("clicks", 0),
            "Gasto": stats.get("spent", 0),
            "CPC Promedio": stats.get("avcpc", 0),
            "Decisiones": stats.get("decision", 0),
            "Costo Decisión": stats.get("decisionCost", 0),
            "Compras": stats.get("buying", 0),
            "Costo Compra": stats.get("buyingCost", 0),
            "Revenue": stats.get("revenue", 0),
            "EPC": stats.get("epc", 0),
            "Profit": stats.get("profit", 0),
        })

    # Crear DataFrame
    df = pd.DataFrame(registros)
    print("\n✅ Muestra de datos:")
    print(df.head())

    # Guardar en Excel
    df.to_excel("estadisticas_mgid.xlsx", index=False)
    print("\n📊 Archivo 'estadisticas_mgid.xlsx' guardado con éxito.")
    return df


# === EJECUCIÓN ===
obtener_estadisticas(api_id)

# import requests
# import json

# # === ⚙️ CONFIGURACIÓN GENERAL ===
# API_BASE_URL = "https://api.mgid.com/v1/goodhits"
# CLIENT_ID = "730589"  # Tu clientId real
# TOKEN = "06426fb424b53f2e9b3753a6694f7ef2"  # Tu token válido

# # === 📅 FECHAS A CONSULTAR ===
# start_date = "2025-02-01"
# end_date = "2025-10-15"

# # === 🌐 ENDPOINT CORRECTO ===
# url = f"{API_BASE_URL}/clients/{CLIENT_ID}/campaigns-stat"

# # === 🧾 CABECERAS ===
# headers = {
#     "Accept": "application/json",
#     "Authorization": f"Bearer {TOKEN}"
# }

# # === 📦 PARÁMETROS DE CONSULTA ===
# params = {
#     "dateInterval": "interval",
#     "startDate": start_date,
#     "endDate": end_date
# }

# print("🔄 Consultando estadísticas de campañas...")
# print(f"📅 Rango de fechas: {start_date} → {end_date}\n")

# # === 🚀 SOLICITUD GET ===
# response = requests.get(url, headers=headers, params=params)

# if response.status_code != 200:
#     print(f"❌ Error {response.status_code}: {response.text}")
#     exit()

# stats_data = response.json()
# campaigns_data = stats_data.get("campaigns-stat", {})

# if not campaigns_data:
#     print("⚠️ No hay datos de campañas en la respuesta.")
# else:
#     print("--- 📊 Detalle por campaña y fecha ---\n")
#     for campaign_id, stats in campaigns_data.items():
#         print(f"📢 Campaña ID: {campaign_id}")
#         intervals = stats.get("interval", [])
#         if not intervals:
#             print("   ⚠️ No hay datos por día en el rango.\n")
#             continue
        
#         for day in intervals:
#             date = day.get("date", "Sin fecha")
#             imps = day.get("imps", 0)
#             clicks = day.get("clicks", 0)
#             spent = day.get("spent", 0)
#             avcpc = day.get("avcpc", 0)
#             revenue = day.get("revenue", 0)
#             profit = day.get("profit", 0)

#             print(f"   📆 {date}")
#             print(f"      👁️ Impresiones: {imps:,}")
#             print(f"      🖱️ Clics: {clicks:,}")
#             print(f"      💰 Gasto: ${spent:,.2f}")
#             print(f"      ⚙️ CPC Promedio: ${avcpc:,.2f}")
#             print(f"      💵 Revenue: ${revenue:,.2f}")
#             print(f"      📈 Profit: ${profit:,.2f}")
#         print("──────────────────────────────\n")
