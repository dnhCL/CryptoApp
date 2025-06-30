import os
import json
from tabulate import tabulate

SNAPSHOT_DIR = "snapshots"

def cargar_snapshots():
    archivos = sorted([f for f in os.listdir(SNAPSHOT_DIR) if f.endswith(".json")])
    snapshots = []
    for archivo in archivos:
        with open(os.path.join(SNAPSHOT_DIR, archivo), "r") as f:
            data = json.load(f)
            snapshots.append({"archivo": archivo, **data})
    return snapshots

def comparar_snapshots(s1, s2):
    tokens1 = {item["Token"]: item for item in s1["analisis_tecnico"]}
    tokens2 = {item["Token"]: item for item in s2["analisis_tecnico"]}

    comparacion = []
    for token in tokens1:
        if token not in tokens2:
            continue

        estado_rsi_1 = tokens1[token]["Estado RSI"]
        estado_rsi_2 = tokens2[token]["Estado RSI"]
        estado_macd_1 = tokens1[token]["Estado MACD"]
        estado_macd_2 = tokens2[token]["Estado MACD"]

        cambio_tecnico = ""
        if estado_rsi_1 != estado_rsi_2 or estado_macd_1 != estado_macd_2:
            cambio_tecnico = "⚠️ CAMBIO"

        dif = {
            "Token": token,
            "RSI Δ": round(tokens2[token]["RSI"] - tokens1[token]["RSI"], 2),
            "MACD Δ": round(tokens2[token]["MACD"] - tokens1[token]["MACD"], 5),
            "EMA Δ": round(tokens2[token]["EMA20"] - tokens1[token]["EMA20"], 5),
            "Promedio Δ": round(tokens2[token]["Promedio %"] - tokens1[token]["Promedio %"], 5),
            "Volatilidad Δ": round(tokens2[token]["Volatilidad %"] - tokens1[token]["Volatilidad %"], 5),
            "Estado RSI": f"{estado_rsi_1} → {estado_rsi_2}",
            "Estado MACD": f"{estado_macd_1} → {estado_macd_2}",
            "Cambio Técnico": cambio_tecnico
        }
        comparacion.append(dif)

    return comparacion

if __name__ == "__main__":
    snapshots = cargar_snapshots()
    if len(snapshots) < 2:
        print("Necesitás al menos 2 snapshots para comparar.")
    else:
        anterior, actual = snapshots[-2], snapshots[-1]
        print(f"\n📚 Comparando: {anterior['archivo']} ⟶ {actual['archivo']}")

        if "valor_total_portafolio" in anterior and "valor_total_portafolio" in actual:
            v_anterior = anterior["valor_total_portafolio"]
            v_actual = actual["valor_total_portafolio"]
            variacion = round(v_actual - v_anterior, 2)
            pct = round((variacion / v_anterior) * 100, 2) if v_anterior else 0
            print(f"💼 Patrimonio total: {v_anterior} → {v_actual} USDT  ({'+' if variacion >=0 else ''}{variacion} USDT, {pct}%)")

        diferencias = comparar_snapshots(anterior, actual)
        print("\n📈 Cambios técnicos detectados:\n")
        print(tabulate(diferencias, headers="keys", tablefmt="fancy_grid"))
