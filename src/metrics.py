def calcular_metricas(procesos):
    total_respuesta = total_retorno = total_espera = 0
    n = len(procesos)
    for p in procesos:
        respuesta = p.tiempo_inicio - p.tiempo_llegada
        retorno = p.tiempo_fin - p.tiempo_llegada
        espera = retorno - p.duracion
        total_respuesta += respuesta
        total_retorno += retorno
        total_espera += espera
    return {
        "respuesta_prom": total_respuesta / n,
        "retorno_prom": total_retorno / n,
        "espera_prom": total_espera / n,
    }
