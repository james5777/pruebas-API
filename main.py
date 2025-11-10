import adcash_API as ac
import sportradar_API as sr
import mgid_API as mg
import propellerads_API as pa
import taboola_API as tb
import tik_tok_API as tt

if __name__ == "__main__":
    # Obtener datos de Ad Cash
    df_ad_cash = ac.obtener_datos_ad_cash()

    # # Obtener datos de Sportradar
    # df_sportradar = sr.obtener_datos_sportradar()

    # Obtener datos de MGID
    df_mgid = mg.obtener_datos_mgid()

    # Obtener datos de PropellerAds
    df_propellerads = pa.obtener_datos_propellerads()

    # Obtener datos de Taboola
    df_taboola = tb.obtener_datos_taboola()

    # Obtener datos de TikTok
    df_tiktok = tt.obtener_datos_tiktok()