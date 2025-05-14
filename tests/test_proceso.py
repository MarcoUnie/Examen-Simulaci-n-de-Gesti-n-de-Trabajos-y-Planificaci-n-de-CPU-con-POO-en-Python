import pytest
from src.proceso import Proceso

def setup_function():
    Proceso.limpiar_pids()

def test_proceso_valido():
    p = Proceso("P1", 5, 1)
    assert p.pid == "P1"
    assert p.duracion == 5

def test_pid_duplicado():
    Proceso("P1", 4, 2)
    with pytest.raises(ValueError):
        Proceso("P1", 3, 3)
