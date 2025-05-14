import pytest
from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler

@pytest.fixture(autouse=True)
def limpiar_pids():
    Proceso.limpiar_pids()

def test_fcfs_scheduler_planifica_correctamente():
    p1 = Proceso("P1", 3, 1)
    p2 = Proceso("P2", 2, 2)
    scheduler = FCFSScheduler()
    resultado = scheduler.planificar([p1, p2])

    assert resultado == [("P1", 0, 3), ("P2", 3, 5)]
    assert p1.tiempo_inicio == 0
    assert p2.tiempo_fin == 5

def test_round_robin_scheduler_planifica_correctamente():
    p1 = Proceso("P1", 5, 1)
    p2 = Proceso("P2", 3, 1)
    scheduler = RoundRobinScheduler(quantum=2)
    resultado = scheduler.planificar([p1, p2])

    assert resultado == [
        ("P1", 0, 2),
        ("P2", 2, 4),
        ("P1", 4, 6),
        ("P2", 6, 7),
        ("P1", 7, 8)
    ]
    assert p1.tiempo_fin == 8
    assert p2.tiempo_fin == 7
