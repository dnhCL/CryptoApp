import sqlite3
import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import EMAIndicator, MACD
from ta.volatility import AverageTrueRange

DB_PATH = "precios.db"

def interpretar_rsi(valor):
    if valor < 30:
        return "🔵 Sobrevendido"
    elif valor > 70:
        return "🔴 Sobrecomprado"
    else:
        return "⚪ Neutro"

def interpretar_macd(macd_val, signal_val):
    return "📉 Bajista" if macd_val < signal_val else "📈 Alcista"

def interpretar_precio_vs_ema(precio, ema):
    return "🔻 Bajo EMA" if precio < ema else "🔺 Sobre EMA"

def analizar_token(token):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"""
    SELECT timestamp, close, high, low
    FROM precios_historicos
    WHERE token = '{token}'
    ORDER BY timestamp ASC
    """, conn)
    conn.close()

    if len(df) < 30:
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["pct_change"] = df["close"].pct_change() * 100

    # RSI
    rsi = RSIIndicator(close=df["close"], window=14).rsi().iloc[-1]
    estado_rsi = interpretar_rsi(rsi)

    # EMA
    ema20 = EMAIndicator(close=df["close"], window=20).ema_indicator().iloc[-1]
    precio_actual = df["close"].iloc[-1]
    estado_ema = interpretar_precio_vs_ema(precio_actual, ema20)

    # MACD
    macd_calc = MACD(close=df["close"])
    macd_val = macd_calc.macd().iloc[-1]
    signal_val = macd_calc.macd_signal().iloc[-1]
    estado_macd = interpretar_macd(macd_val, signal_val)

    # ATR
    atr = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14).average_true_range().iloc[-1]

    # Estadísticas básicas
    total = len(df) - 1
    subidas = df["pct_change"].gt(0).sum()
    bajadas = df["pct_change"].lt(0).sum()
    promedio = df["pct_change"].mean()
    std_dev = df["pct_change"].std()
    df["rolling_max"] = df["close"].rolling(window=24).max()
    df["drawdown"] = (df["close"] - df["rolling_max"]) / df["rolling_max"] * 100
    max_drawdown = df["drawdown"].min()

    return {
        "Token": token,
        "Velas": total,
        "Alcistas %": round(subidas / total * 100, 2),
        "Bajistas %": round(bajadas / total * 100, 2),
        "Promedio %": round(promedio, 5),
        "Volatilidad %": round(std_dev, 5),
        "Max Drawdown %": round(max_drawdown, 2),
        "RSI": round(rsi, 2),
        "Estado RSI": estado_rsi,
        "EMA20": round(ema20, 5),
        "Precio vs EMA": estado_ema,
        "MACD": round(macd_val, 5),
        "MACD Señal": round(signal_val, 5),
        "Estado MACD": estado_macd,
        "ATR": round(atr, 5)
    }

def analizar_portafolio():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tokens = [row[0] for row in cursor.execute("SELECT DISTINCT token FROM precios_historicos WHERE token IS NOT NULL")]

    conn.close()

    resumen = [analizar_token(t) for t in tokens]
    return [r for r in resumen if r is not None]
