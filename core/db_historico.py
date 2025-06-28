import sqlite3
import time
from datetime import datetime
from config import crear_cliente
from binance_utils import obtener_balances_activos

# Configuración
DB_PATH = "precios.db"
INTERVALO = "1h"
LIMITE = 1000

# Crear cliente Binance
client = crear_cliente()

# Obtener tokens con saldo
balances = obtener_balances_activos(client)
tokens = [b["asset"] for b in balances if b["asset"] != "USDT"]

# Conectar a DB y preparar tabla
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS precios_historicos (
    token TEXT,
    timestamp DATETIME,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    PRIMARY KEY (token, timestamp)
);
""")
conn.commit()

# Descargar y guardar klines por token
for symbol in tokens:
    pair = f"{symbol}USDT"
    try:
        klines = client.klines(symbol=pair, interval=INTERVALO, limit=LIMITE)
    except Exception as e:
        print(f"[!] Error al obtener {pair}: {e}")
        continue

    count = 0
    for k in klines:
        timestamp = datetime.fromtimestamp(k[0] / 1000)
        open_, high, low, close, volume = float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5])

        cursor.execute("""
        INSERT OR IGNORE INTO precios_historicos (token, timestamp, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pair, timestamp, open_, high, low, close, volume))
        count += 1

    conn.commit()
    print(f"[✓] {pair} guardado ({count} registros)")
    time.sleep(0.5)  # para evitar límite de API

conn.close()
print("\n✅ Finalizado.")
