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