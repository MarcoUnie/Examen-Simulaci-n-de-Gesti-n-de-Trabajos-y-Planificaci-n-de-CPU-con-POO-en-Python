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
        gantt: List[GanttEntry] = []

        for proceso in procesos:
            proceso.tiempo_inicio = tiempo_actual
            tiempo_fin = tiempo_actual + proceso.duracion
            proceso.tiempo_fin = tiempo_fin
            proceso.tiempo_restante = 0

            gantt.append((proceso.pid, proceso.tiempo_inicio, proceso.tiempo_fin))
            tiempo_actual = tiempo_fin

        return gantt


class RoundRobinScheduler(Scheduler):
    def __init__(self, quantum: int = 2):
        self.quantum = quantum

    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        gantt: List[GanttEntry] = []
        tiempo_actual = 0

        # Inicializamos tiempo restante si no está
        for proceso in procesos:
            proceso.tiempo_restante = proceso.duracion

        cola = procesos[:]
        while cola:
            proceso = cola.pop(0)

            if proceso.tiempo_restante > 0:
                if proceso.tiempo_inicio is None:
                    proceso.tiempo_inicio = tiempo_actual

                tiempo_ejecucion = min(self.quantum, proceso.tiempo_restante)
                tiempo_fin = tiempo_actual + tiempo_ejecucion

                gantt.append((proceso.pid, tiempo_actual, tiempo_fin))

                proceso.tiempo_restante -= tiempo_ejecucion
                tiempo_actual = tiempo_fin

                if proceso.tiempo_restante > 0:
                    cola.append(proceso)
                else:
                    proceso.tiempo_fin = tiempo_actual

        return gantt
