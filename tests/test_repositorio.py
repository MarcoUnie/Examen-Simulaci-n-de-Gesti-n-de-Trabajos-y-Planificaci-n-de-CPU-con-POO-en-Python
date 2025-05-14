import pytest
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos

@pytest.fixture(autouse=True)
def limpiar_pids():
    Proceso.limpiar_pids()

def test_agregar_y_obtener_proceso():
    repo = RepositorioProcesos()
    p = Proceso("P1", 4, 1)
    repo.agregar(p)

    assert repo.obtener("P1") == p
    assert len(repo.listar()) == 1

def test_eliminar_proceso():
    repo = RepositorioProcesos()
    p = Proceso("P1", 4, 1)
    repo.agregar(p)
    repo.eliminar("P1")
    assert repo.obtener("P1") is None

def test_guardar_y_cargar_json(tmp_path):
    repo1 = RepositorioProcesos()
    repo1.agregar(Proceso("P1", 5, 1))
    json_file = tmp_path / "procesos.json"
    repo1.guardar_json(json_file)

    repo2 = RepositorioProcesos()
    repo2.cargar_json(json_file)

    assert len(repo2.listar()) == 1
    assert repo2.obtener("P1").duracion == 5

def test_guardar_y_cargar_csv(tmp_path):
    repo1 = RepositorioProcesos()
    repo1.agregar(Proceso("P1", 5, 1))
    csv_file = tmp_path / "procesos.csv"
    repo1.guardar_csv(csv_file)

    repo2 = RepositorioProcesos()
    repo2.cargar_csv(csv_file)

    assert len(repo2.listar()) == 1
    assert repo2.obtener("P1").duracion == 5
