import sqlite3
import pandas as pd

DB_PATH = "precios.db"

def resumen_por_token():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT 
            token,
            COUNT(*) AS registros,
            MIN(timestamp) AS fecha_inicial,
            MAX(timestamp) AS fecha_final
        FROM precios_historicos
        GROUP BY token
        ORDER BY token
    """, conn)
    conn.close()
    return df

if __name__ == "__main__":
    resumen = resumen_por_token()
    print("\n📊 Estado de la base de datos:\n")
    print(resumen.to_string(index=False))
