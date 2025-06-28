import time
import json
from datetime import datetime

def obtener_balances_activos(client):
    account = client.account()
    return [
        b for b in account["balances"]
        if float(b["free"]) > 0
    ]

def obtener_valor_en_usdt(client, balances):
    total = 0.0
    precios_unitarios = {}

    for asset in balances:
        symbol = asset["asset"]
        amount = float(asset["free"])

        if symbol == "USDT":
            price = 1.0
        else:
            try:
                ticker = client.ticker_price(symbol=f"{symbol}USDT")
                price = float(ticker["price"])
            except:
                continue

        precios_unitarios[symbol] = price
        total += price * amount

    return precios_unitarios, round(total, 2)


def obtener_promedio_compra(client, symbol):
    trades = client.my_trades(symbol=symbol)
    total_qty = 0.0
    total_cost = 0.0

    for t in trades:
        if t["isBuyer"]:
            qty = float(t["qty"])
            price = float(t["price"])
            total_qty += qty
            total_cost += qty * price

    return total_cost / total_qty if total_qty > 0 else None

def calcular_precios_entrada(client, balances, guardar_en_archivo=False):
    precios = {}
    for asset in balances:
        symbol = asset["asset"]
        if symbol == "USDT":
            continue

        pair = f"{symbol}USDT"
        try:
            promedio = obtener_promedio_compra(client, pair)
            if promedio:
                precios[symbol] = round(promedio, 4)
        except:
            continue
        time.sleep(0.2)

    if guardar_en_archivo:
        with open("precios_entrada.json", "w") as f:
            json.dump(precios, f, indent=2)

    return precios




def obtener_historial_trades(client, symbol_pair):
    trades = client.my_trades(symbol=symbol_pair)
    historial = []

    for t in trades:
        historial.append({
            "fecha": datetime.fromtimestamp(t["time"] / 1000).strftime("%Y-%m-%d %H:%M"),
            "tipo": "COMPRA" if t["isBuyer"] else "VENTA",
            "precio": float(t["price"]),
            "cantidad": float(t["qty"]),
            "total_usdt": float(t["quoteQty"])
        })

    return historial