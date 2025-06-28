import os
from core.config import crear_cliente
from core.binance_utils import (
    obtener_balances_activos,
    obtener_valor_en_usdt,
    calcular_precios_entrada,
)
from core.rendimiento import calcular_rendimiento_por_token

def obtener_estado_portafolio():
    client = crear_cliente()

    balances = obtener_balances_activos(client)
    precios_actuales, total_portafolio = obtener_valor_en_usdt(client, balances)
    precios_entrada = calcular_precios_entrada(client, balances)

    if "SHIB" not in precios_entrada or precios_entrada["SHIB"] == 0:
        precios_entrada["SHIB"] = 0.00001669

    rendimientos = calcular_rendimiento_por_token(balances, precios_actuales, precios_entrada)

    # Análisis técnico solo si existe la base de datos
    comportamiento = []
    if os.path.exists("precios.db"):
        from core.analisis_portafolio import analizar_portafolio
        comportamiento = analizar_portafolio()
    else:
        comportamiento = [{"info": "Base de datos histórica no disponible en entorno actual."}]

    return {
        "rendimientos": rendimientos,
        "comportamiento": comportamiento,
        "total": total_portafolio
    }
