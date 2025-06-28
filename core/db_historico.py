import sqlite3
from datetime import datetime
from binance.spot import Spot
import time

client = Spot()

DB_PATH = "precios.db"
INTERVALO = "1h"
LIMITE = 1000

def crear_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS precios_historicos (
        token TEXT,
        timestamp TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL,
        PRIMARY KEY (token, timestamp)
    )
    """)
    conn.commit()
    conn.close()

def descargar_guardar_klines(token_base):
    symbol = f"{token_base}USDT"
    try:
        klines = client.klines(symbol=symbol, interval=INTERVALO, limit=LIMITE)
    except Exception as e:
        print(f"❌ Error al obtener datos de {symbol}: {e}")
        return

    registros = []
    for k in klines:
        timestamp = datetime.utcfromtimestamp(k[0] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        registros.append((
            token_base,  # ✅ Guardar solo el token base, no el par completo
            timestamp,
            float(k[1]),  # open
            float(k[2]),  # high
            float(k[3]),  # low
            float(k[4]),  # close
            float(k[5])   # volume
        ))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    nuevos = 0
    for r in registros:
        try:
            cursor.execute("""
            INSERT INTO precios_historicos (token, timestamp, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, r)
            nuevos += 1
        except sqlite3.IntegrityError:
            continue

    conn.commit()
    conn.close()
    print(f"✅ {token_base}USDT: {nuevos} registros nuevos añadidos.")

def actualizar_todos_los_tokens(tokens):
    crear_db()
    for token in tokens:
        descargar_guardar_klines(token)
        time.sleep(0.5)

def actualizar_db_desde_main():
    mis_tokens = [
        "SHIB", "ADA", "TRX", "THETA", "FET", "ONE", "WIN", "EUR",
        "LUNA", "CAKE", "LUNC", "WLD", "NOT", "ACT"
    ]
    actualizar_todos_los_tokens(mis_tokens)

if __name__ == "__main__":
    actualizar_db_desde_main()
