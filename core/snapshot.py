import os
import json
from datetime import datetime
from core.analisis_portafolio import analizar_portafolio
from core.resumen_db import resumen_por_token
from core.servicio import obtener_estado_portafolio


SNAPSHOT_DIR = "snapshots"

def guardar_snapshot_actual():
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    archivo_nombre = f"snapshot_{datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    archivo_path = os.path.join(SNAPSHOT_DIR, archivo_nombre)

    analisis = analizar_portafolio()
    resumen = resumen_por_token()

    datos = obtener_estado_portafolio()  # 🆕 obtenemos el total
    snapshot = {
        "timestamp": timestamp,
        "valor_total_portafolio": datos["total"],  # 🆕 se guarda el valor total aquí
        "base_historica": resumen.to_dict(orient="records"),
        "analisis_tecnico": analisis
    }

    with open(archivo_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"💾 Snapshot guardado: {archivo_path}")
