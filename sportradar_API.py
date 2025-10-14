# import requests
# import pandas as pd

# # === Credenciales ===
# REFRESH_TOKEN = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.n1seeohBbBHNLZ-BKfQWSf_gFONZte5A1dXTco3HNA2pJsRtHcbt3vG7lHM33bYQTryKYIqP7XUFw8rFk_-T-B6VNwjOT0gPsgWax8nn6tA3uHPEGBFgxzian2vs_4s6N1Na8aUrWB7Gz_7t08bduYcn_vxN6Bhy2KFECAfj7vAO3rwmIzJRiNYFwE_M6ibAQyalYrrHaDgBwGChNKWnhV8FG2n1kv-0Cg2_xzHDEv3Bzd90blyLYTt_a_j9EqoxgfmyLgjGMdNOOS4xi7iC27JmiOITlktMia-17avswgZyAdyDNQKPaVVcJqWFojeD8RQdN982XNJlf_bwRbz3hg.b6OMhgJ4oyQQiMcq._6jWOQXQOtg-OzNB8yJ5x-bnNG999YlFTNZ_nDreBtAi19kvry72KhkF9NrGpCPp2thAWra5i8yP8h5RfbN1XbL-I-OSUBoiX_gANrnOeTWJsgmTsc2jW-vxTn0k3KlPnTEmjCpWM742OqsdJ9BnRHk-_99EeY6UQwhnml2czGx-BYtJF73a698x6tys_w2a2vrgAcTRkg6K0yulMQVJDpzk49b4CrBfg-c9-iNzhs7pyX0iFlgPFSkpq6FVkkBk9vhP_bu-ygUEo0FXAPf6SjqvJhx2_aruqkeJMtQ343kjmnxrlTyUMLO0rkjMb99yIpPxag0_iY7Q4RvqWQyWN1aZYB6L-n78pM11qeoS68O9-BCxvImmo2e20oLsZpEKvvO-f2J0ZVgR_JqOBs8pEA11lE4NaUP5rd6MUEWhIepC4VqgZ08Vqc1HsE7xxj8MCTF1VE5fZIdlasp-tLSXiKBM_UcOM5yxIMAYDw7tc38YePHGBTNrcpZEqJh1O6_p2UWJyiTsVKNKrStkfuUogRTjy1qhTMifpRXIzlMX8YE7b1kKVzt2yk2ITQas6lYIeb6GxDmT-seSrugl0hKgs_5QaNwC_UeFJwVWPV6s6RAcaz8Go7XjZQGF8UamOMx1kI2Y42blqnzAmzHZ9I8sbvriasj7ZU6rdA-OOfMXDzNRgI1-ETUPbmhMk2GiIELofaT6GRdPl6bmikpH8ssy6yYMtLePXJ1ESt96b36UKGDLgd_QrK-4xJhlbAiv10u3vTFN379Rjh1zS1mkoA6zFDb_zQy7iMVyKlFIRmXcuWQSYp5VbJlaoa7cYkk0TGDmNCbDftiIYqr9cnuAB57GyEjsnvst0b96HrESl5n1NYVXAGQk9J0tZu6GEX2w5LHBsVBD8OREEnNppKgzWLFF1MBslXAqxHSbuSQH0ko7XqKTtopmvGcQJXoLp_rP1n9WlpuJ9_4qh67pmP77Pnw_oSlMTPzCS4cWaZj0vla7JKuluKSD4knyJuF8WhWAulxACzt7E2_mFWT9BHGo7d3hLfsF3WBHjcT0gp9ndKFLHh5PnZKBbvk1MaIpvh_R5wOL1RkAXsxHXBqpCWe26GFCnr0FUZqWlmfnM-c0DCfFp9LstI__p2rwJeagtZF8EOpeTYvkUnmKIHX2Gy2JOItKiU2hALqfexdOQWRrKDH4qe0wjnFX0heHJBWGrRVUddsGlJDlrGDJNkIn8HDvQRj3b93snZQUdeKcR-Slo4hRWQRxOk8W6edge_0mFmx9hyDv3Dw.37PDv92uLXqa0F0DoXe-4g"
# ID_TOKEN = "eyJraWQiOiJsMDdheTRNdEhWTWEwTDdvZEVReUorNUg1OHI1R2syaU1lK0dORTNCenV3PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiUnZudjB6bzJ3dlV1aWRIRlpCamFNUSIsInN1YiI6IjRiZTZjODhlLWI1NWUtNDU5YS1hY2IxLWY1NWIxYzY3MDE4ZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9XNWF4YWFxMWwiLCJjb2duaXRvOnVzZXJuYW1lIjoiNGJlNmM4OGUtYjU1ZS00NTlhLWFjYjEtZjU1YjFjNjcwMThkIiwib3JpZ2luX2p0aSI6ImZjMWIzZWRjLTUyNmQtNGEyYi04MGQ5LTcyNDBjMGEzYWU3YSIsImF1ZCI6IjF0YzM3aTVvaWhucjA0YmNpcTMzMzBkbHRvIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NjA0NjM5MjUsIm5hbWUiOiJUaGVvZG9ybyIsImV4cCI6MTc2MDU1MDMyNSwiaWF0IjoxNzYwNDYzOTI1LCJmYW1pbHlfbmFtZSI6IkRpa3V5YW1hIiwianRpIjoiODVkNjlmMzctNWI2Zi00OWFkLTgzOWYtZTRiMjBiNGRhNmMyIiwiZW1haWwiOiJ0aGVvZG9yby5kaWt1eWFtYUBxdW90YW1lZGlhLmNvIn0.nVsC5_fIi2MDTdeC_eDZzYVl5Z-gpxwFTLWQmw_mhS0wMRzDwi6Zi8kvw1wUIolCNgR02y_ibUqnn2qlh2Ipd0rwPTNqgh7Nj1xFSuwtb2SvrCD-X8JG-Q_Nbd6q88JDEv1IL-6euXI2TEIr5jTq1NeQnh8sBZ_yU_bmxjvxSI2AJIGcpx1ODkM3BpbvipTGuYjE71lgfoGLHE0tO9aRXq96aS-J9SIIDGwK2xJGznvud_x7Q2RH9syCA-b_TImS9JkhNmJpTv2zgS3lq7TdGZe-4wPsL637HK10HFirRAwcYSvcMzgXTVYTQS83q6f24SvUEBz8nCERde-f3sla2Q"

# # === URL para renovar token ===
# token_url = "https://api.api-access.iam.ads.sportradar.com/prod/oauth2/token"

# headers = {
#     "Authorization": f"Bearer {ID_TOKEN}",
#     "Content-Type": "application/json"
# }

# body = {
#     "refreshToken": REFRESH_TOKEN
# }

# # === Solicitar nuevo token ===
# response = requests.post(token_url, headers=headers, json=body)
# print("🔎 Status:", response.status_code)
# print("🔎 Respuesta:", response.text)

# if response.status_code == 200:
#     new_token = response.json().get("idToken")
#     print("✅ Nuevo token obtenido correctamente:")
#     print(new_token)
# else:
#     print("❌ Error al obtener token:", response.text)


import requests
import datetime
import pandas as pd

# Datos iniciales
id_token = "eyJraWQiOiJsMDdheTRNdEhWTWEwTDdvZEVReUorNUg1OHI1R2syaU1lK0dORTNCenV3PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiYjQ0dExKeEFmbFZVTFNJYTlfSFA3USIsInN1YiI6IjRiZTZjODhlLWI1NWUtNDU5YS1hY2IxLWY1NWIxYzY3MDE4ZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9XNWF4YWFxMWwiLCJjb2duaXRvOnVzZXJuYW1lIjoiNGJlNmM4OGUtYjU1ZS00NTlhLWFjYjEtZjU1YjFjNjcwMThkIiwib3JpZ2luX2p0aSI6ImRkZWY2Yzg3LTc5YmEtNDZhNi1hZTFkLTlkZmMxYTYwNmI4YiIsImF1ZCI6IjF0YzM3aTVvaWhucjA0YmNpcTMzMzBkbHRvIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NjA0NjQzMTEsIm5hbWUiOiJUaGVvZG9ybyIsImV4cCI6MTc2MDU1MDcxMSwiaWF0IjoxNzYwNDY0MzExLCJmYW1pbHlfbmFtZSI6IkRpa3V5YW1hIiwianRpIjoiYzNlODU2MGEtOGI1Mi00Yzg4LWFhODItYjBiYWQwNjA2MTA3IiwiZW1haWwiOiJ0aGVvZG9yby5kaWt1eWFtYUBxdW90YW1lZGlhLmNvIn0.If5g0SKFhsFm85nwC-qpSi52cmQDY5gxje_tdIXS0uBGRhBBA5avCKup4Xhhanz8CtdAIMWbGvn8Pa2IbUTD7KrP6ofU2FP-orZD6RpmxhPwsc32Oi494VLawqxxrmSq9KJHkFmSeU6eghvzqIhSMg_7o8cd2k9hCE8MEG73tFth_SWRJQnI_Sl1hKKNynxem8rpgFlOxqD6EEPxk4nXvbAkvkUFDw7zJOH5fvgGlzARd5jbZ0owLOS2npxXalYeFB-5RLcUmsacSRW3Hlg2NhOxEyEUGQ6_iyUaGqA-CPAsYtVbhsUJWEVIHwLBPuOelPcyhae84ncVU1QJy0daWg"  # tu token actual
refresh_token = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.qMluKGaFjSvkmtZ8BA-aNxT1k3oJNQ4ejuIpAyNfkKBegwzccav4TiFlEZSbIpwwIZrgEKcNGR03r3E1pdGYlmPNyc6ou7wCasN0QQO9ewDPSbTG2jAotXGD1GKsOBlHG5w1YWr4dZKX5_7MWLNBHVbVEEnFlxw-VE-ls2SbmeeIctdeHw7EBIJkmYKKVqVn2kDmJLo5AqADDXKrF93X6I4skJtn0wp7aM5pWtS7M9eIY7TfVBRPu-L8W0AMvP3cg2MhI3ObpDjJwICaYOvKxU-iu2dnN2Cfr087NOFovGMUv_g9PnKSmlW5JM44K82GfV7DpOnvbJDn72BJmxmUpg.2TdhZrHEZVsBUxgg.447u-R7e00wu3yKz6a-0YEWkIRgQ1WCuCDrzq6BRRhQJ_vzVux0GQJe2vwrVKODk4WrKs6kukcpXEJDDeK2zEY8inbYqy_XMZIYvsSMxxSdGhjAOmyeS3B9D1-AUKAqV4quxOA9fYVCdNTtCsDmW8INOzKuF4n3ZGC93SBlM5c8b07LsKqygB8Nk2ZYVmZGwmhykEegqHUa9tTSJryjkOnap5fntTQb5RKA6ZKCHUjTUK4s1lgF_bsv3TJlm62A3SQ-4ljcsgj7-rayfjxIW5OUZkEz6pP2eeMEiQUvdX3_V-Mx4ECdrAWqkiJOp0aOtYB2TOPEFWDadU9CpqG9Hmb4WGkMDIN87UMyW_oU-SXaCE9apiqJ950ouHzNj-xR_PgM_873Q4VKloDZMzS1CqBlxmPE2nPBsUGhT_eJdm6aWkOR9Od2sulS7K0uiDCKaiERe_qGgW6w3BGH0kY-L0mcJ14c8SDRmMiELRorH3IOlG48gfxS_eQ-8EK1AFxh-Uy9Mj-_dOHl4y_CwHpZEWUL6DSwFJRsNTCfcZ4030Pw2MMvSTxPTqeKiErVED2ld7LeWhGq_5NMMbmzG0SKidXxig8QJrOQyZagDEyZeH5HN6stUqXl68n7qZ_ChFQgH6eP9mb7CwZ-9xPWHCHzLQdla7ThsCbCAVyhbIZhxN8icfidfErZu5YOHdz2fy-anY35Q4sibRunynSqu8xPL03O_uO8ITafzn3sIPsQwVpoL3AnvF2dI3U-h1VcvK50V43CnrdhdC5KML6Mzgu3u0Qu02O6vlGX-mv_2Ps5fPjhuXJCloDcvZv0abWJ5oLZIy2Ve2haeS0cQAIAGeEpMuYgXexTHH9Yf4-7n68qO9DB6ybnOoedX9XQmBoB8qiXgLnVyb-Klzl0qC8STprHOXvhRooGl_tZvcwO8KE5gRHGbrry9E9kTZvS6S78Jb3qk3ny0AiSvZgsAJOnQUSo-8OXrvHCvyARveaFYsNharpeMNgprn2z0kl6W2wr7rmwwjC2-bG5IGcC6m-DKmtf6ij7Gk9VUkepA9_pLi9uptyUVylhHlczbvhUXVy66mlZP3rcFky_Mg9eYzfaaJRwk1-SL5A5RvC1EAbpc8Y9YccG94fVc3CnueSSxi3EAqWnIy3j1noZOgbdjOG1WcJjhoiLxUF3F0I8AyML-kCRRGFB_SGoYNTRQbKtBbY6BeKoWnfzLdVS7jTYx8Erhys9fYH2dSeKMOU4WFPOY__J0KmdwcgcPw5VsKx4YPFO0E5HviKk.FpmJa8WQY_3c1_y0ho4nHw"  # lo que te da el sistema al generar el token
token_expiration = datetime.datetime.now() + datetime.timedelta(hours=6)

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

def get_data_from_api():
    if datetime.datetime.now() >= token_expiration:
        refresh_id_token()

    headers = {"Authorization": f"Bearer {id_token}"}
    url = "https://api.reporting-studio.ads.sportradar.com/..."  # endpoint específico
    response = requests.get(url, headers=headers)
    return response.json()


import requests

url = "https://api.reporting-studio.ads.sportradar.com/grid"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJraWQiOiJsMDdheTRNdEhWTWEwTDdvZEVReUorNUg1OHI1R2syaU1lK0dORTNCenV3PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiYjQ0dExKeEFmbFZVTFNJYTlfSFA3USIsInN1YiI6IjRiZTZjODhlLWI1NWUtNDU5YS1hY2IxLWY1NWIxYzY3MDE4ZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9XNWF4YWFxMWwiLCJjb2duaXRvOnVzZXJuYW1lIjoiNGJlNmM4OGUtYjU1ZS00NTlhLWFjYjEtZjU1YjFjNjcwMThkIiwib3JpZ2luX2p0aSI6ImRkZWY2Yzg3LTc5YmEtNDZhNi1hZTFkLTlkZmMxYTYwNmI4YiIsImF1ZCI6IjF0YzM3aTVvaWhucjA0YmNpcTMzMzBkbHRvIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NjA0NjQzMTEsIm5hbWUiOiJUaGVvZG9ybyIsImV4cCI6MTc2MDU1MDcxMSwiaWF0IjoxNzYwNDY0MzExLCJmYW1pbHlfbmFtZSI6IkRpa3V5YW1hIiwianRpIjoiYzNlODU2MGEtOGI1Mi00Yzg4LWFhODItYjBiYWQwNjA2MTA3IiwiZW1haWwiOiJ0aGVvZG9yby5kaWt1eWFtYUBxdW90YW1lZGlhLmNvIn0.If5g0SKFhsFm85nwC-qpSi52cmQDY5gxje_tdIXS0uBGRhBBA5avCKup4Xhhanz8CtdAIMWbGvn8Pa2IbUTD7KrP6ofU2FP-orZD6RpmxhPwsc32Oi494VLawqxxrmSq9KJHkFmSeU6eghvzqIhSMg_7o8cd2k9hCE8MEG73tFth_SWRJQnI_Sl1hKKNynxem8rpgFlOxqD6EEPxk4nXvbAkvkUFDw7zJOH5fvgGlzARd5jbZ0owLOS2npxXalYeFB-5RLcUmsacSRW3Hlg2NhOxEyEUGQ6_iyUaGqA-CPAsYtVbhsUJWEVIHwLBPuOelPcyhae84ncVU1QJy0daWg",
    "Content-Type": "application/json"
}
payload = {
    "split_by": ["demand.advertiser_id"],
    "start_date": "2025-10-01",
    "end_date": "2025-10-14",
    "timezone": -5
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.json())

data = response.json()
if "rows" in data and len(data["rows"]) > 0:
    rows = data["rows"]
    # Cada fila tiene un array de "data"
    df = pd.DataFrame([
        {d["name"]: d["value"] for d in row["data"]}
        for row in rows
    ])
    print(df.head())
else:
    print("No hay datos en el rango especificado")