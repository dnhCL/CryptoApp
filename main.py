from core.servicio import obtener_estado_portafolio
from tabulate import tabulate
import pandas as pd
from core.db_historico import actualizar_db_desde_main
from core.snapshot import guardar_snapshot_actual
from core.comparar_snapshots import cargar_snapshots, comparar_snapshots

# Actualizar la base de datos con datos históricos recientes
actualizar_db_desde_main()
datos = obtener_estado_portafolio()

# Mostrar resumen financiero
tabla = []
headers = ["Token", "Cantidad", "Precio Entrada", "Precio Actual", "Valor Inicial", "Valor Actual", "Ganancia USDT", "Rendimiento %"]

for r in datos["rendimientos"]:
    fila = [
        r["token"],
        f"{r['cantidad']:.10f}".rstrip('0').rstrip('.'),
        f"{r['precio_entrada']:.10f}".rstrip('0').rstrip('.'),
        f"{r['precio_actual']:.10f}".rstrip('0').rstrip('.'),
        f"{r['valor_inicial']:.2f}",
        f"{r['valor_actual']:.2f}",
        f"{r['ganancia_usdt']:.2f}",
        f"{r['rendimiento_pct']:.2f}"
    ]
    tabla.append(fila)

print("\n📊 Resumen Financiero por Token:\n")
print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
print(f"\n💰 Valor total estimado del portafolio: {datos['total']:.2f} USDT")

# Mostrar análisis técnico
df_analisis = pd.DataFrame(datos["comportamiento"])
print("\n📊 Comportamiento Histórico por Token (1h):\n")
print(df_analisis.to_string(index=False))

guardar_snapshot_actual()

snapshots = cargar_snapshots()
if len(snapshots) >= 2:
    anterior, actual = snapshots[-2], snapshots[-1]
    print(f"\n📚 Comparación con snapshot anterior: {anterior['archivo']} ⟶ {actual['archivo']}")
    diferencias = comparar_snapshots(anterior, actual)
    print("\n📈 Cambios técnicos detectados:\n")
    print(tabulate(diferencias, headers="keys", tablefmt="fancy_grid"))


def sugerencias_toma_ganancias(rendimientos, comportamiento):
    sugerencias = []
    for r in rendimientos:
        token = r["token"]
        ganancia_pct = r["rendimiento_pct"]
        valor_actual = r["valor_actual"]
        ganancia_usdt = r["ganancia_usdt"]

        c = next((item for item in comportamiento if item["Token"] == token), None)
        if not c:
            continue

        rsi = c["RSI"]
        ema20 = c["EMA20"]
        precio_actual = r["precio_actual"]
        estado_macd = c["Estado MACD"]

        if rsi > 70 and "Alcista" in estado_macd and ganancia_usdt > 1:
            # Definir % a retirar
            if 70 < rsi <= 75:
                pct_retirar = 0.3
            elif 75 < rsi <= 80:
                pct_retirar = 0.5
            else:
                pct_retirar = 0.7

            monto_retirar = round(ganancia_usdt * pct_retirar, 2)
            if monto_retirar < 5:
                continue  # Salta tokens con retiro no viable

            monto_reingreso = round(monto_retirar * 0.65, 2)
            sugerencias.append({
                "Token": token,
                "% a Retirar": f"{int(pct_retirar * 100)}%",
                "Monto USDT": monto_retirar,
                "RSI": rsi,
                "EMA20": round(ema20, 5),
                "Reingreso RSI": "<60",
                "Reingreso EMA": f"~{round(ema20*0.99,5)}–{round(ema20*1.01,5)}",
                "Monto Reingreso": monto_reingreso
            })

    return sugerencias



# En el flujo principal
sugerencias = sugerencias_toma_ganancias(datos["rendimientos"], datos["comportamiento"])
if sugerencias:
    from tabulate import tabulate
    print("\n💡 Sugerencias de Toma de Ganancias:\n")
    print(tabulate(sugerencias, headers="keys", tablefmt="fancy_grid"))
else:
    print("\n💡 No hay sugerencias de toma de ganancias en este análisis.")
