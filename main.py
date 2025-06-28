from core.servicio import obtener_estado_portafolio
from tabulate import tabulate
import pandas as pd

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
