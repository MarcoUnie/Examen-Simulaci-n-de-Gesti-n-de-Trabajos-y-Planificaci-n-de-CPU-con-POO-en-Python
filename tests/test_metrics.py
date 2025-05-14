import pytest
from src.proceso import Proceso
from src.metrics import calcular_metricas

@pytest.fixture(autouse=True)
def limpiar_pids():
    Proceso.limpiar_pids()

def test_metricas_calculadas_correctamente():
    p1 = Proceso("P1", 4, 1)
    p1.tiempo_inicio = 0
    p1.tiempo_fin = 4

    p2 = Proceso("P2", 3, 1)
    p2.tiempo_inicio = 4
    p2.tiempo_fin = 7

    metricas = calcular_metricas([p1, p2])

    assert metricas["respuesta_prom"] == pytest.approx(2.0)
    assert metricas["retorno_prom"] == pytest.approx(5.5)
    assert metricas["espera_prom"] == pytest.approx(2.0) 
