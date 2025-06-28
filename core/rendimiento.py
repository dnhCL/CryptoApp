def calcular_rendimiento_por_token(balances, precios_actuales, precios_entrada):
    resultados = []

    for asset in balances:
        symbol = asset["asset"]
        cantidad = float(asset["free"])

        if symbol not in precios_actuales or symbol not in precios_entrada:
            continue

        precio_actual = precios_actuales[symbol]
        precio_entrada = precios_entrada[symbol]

        valor_actual = precio_actual * cantidad
        valor_inicial = precio_entrada * cantidad
        diferencia = valor_actual - valor_inicial
        rendimiento_pct = (diferencia / valor_inicial) * 100 if valor_inicial else 0

        resultados.append({
            "token": symbol,
            "cantidad": cantidad,
            "valor_actual": round(valor_actual, 2),
            "valor_inicial": round(valor_inicial, 2),
            "ganancia_usdt": round(diferencia, 2),
            "rendimiento_pct": round(rendimiento_pct, 2),
            "precio_actual": precio_actual,
            "precio_entrada": precio_entrada
        })

    return resultados
