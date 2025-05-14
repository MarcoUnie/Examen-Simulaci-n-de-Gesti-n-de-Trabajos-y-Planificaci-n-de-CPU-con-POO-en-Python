from abc import ABC, abstractmethod
from typing import List, Tuple
from src.proceso import Proceso

GanttEntry = Tuple[str, int, int]

class Scheduler(ABC):
    @abstractmethod
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        pass

class FCFSScheduler(Scheduler):
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        tiempo_actual = 0
        resultado = []
        for p in procesos:
            p.tiempo_inicio = tiempo_actual
            p.tiempo_fin = tiempo_actual + p.duracion
            resultado.append((p.pid, p.tiempo_inicio, p.tiempo_fin))
            tiempo_actual = p.tiempo_fin
        return resultado

class RoundRobinScheduler(Scheduler):
    def __init__(self, quantum: int):
        self.quantum = quantum

    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        tiempo_actual = 0
        resultado = []
        cola = procesos.copy()

        while any(p.tiempo_restante > 0 for p in cola):
            for p in cola:
                if p.tiempo_restante <= 0:
                    continue
                if p.tiempo_inicio is None:
                    p.tiempo_inicio = tiempo_actual
                ejecutado = min(self.quantum, p.tiempo_restante)
                resultado.append((p.pid, tiempo_actual, tiempo_actual + ejecutado))
                tiempo_actual += ejecutado
                p.tiempo_restante -= ejecutado
                if p.tiempo_restante == 0:
                    p.tiempo_fin = tiempo_actual
        return resultado
