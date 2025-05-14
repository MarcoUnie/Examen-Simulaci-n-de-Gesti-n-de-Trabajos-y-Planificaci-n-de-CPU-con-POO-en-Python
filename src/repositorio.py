import json
import csv
from src.proceso import Proceso

class RepositorioProcesos:
    def __init__(self):
        self.procesos = {}

    def agregar(self, proceso: Proceso):
        if proceso.pid in self.procesos:
            raise ValueError(f"Proceso con PID {proceso.pid} ya existe.")
        self.procesos[proceso.pid] = proceso

    def listar(self):
        return list(self.procesos.values())

    def eliminar(self, pid: str):
        if pid in self.procesos:
            del self.procesos[pid]

    def obtener(self, pid: str):
        return self.procesos.get(pid)

    def guardar_json(self, archivo: str):
        with open(archivo, 'w') as f:
            json.dump([{k: getattr(p, k) for k in ('pid', 'duracion', 'prioridad')} for p in self.procesos.values()], f)

    def cargar_json(self, archivo: str):
        from src.proceso import Proceso
        Proceso.limpiar_pids()
        self.procesos = {}
        with open(archivo) as f:
            datos = json.load(f)
            for d in datos:
                self.agregar(Proceso(**d))

    def guardar_csv(self, archivo: str):
        with open(archivo, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['pid', 'duracion', 'prioridad'])
            for p in self.procesos.values():
                writer.writerow([p.pid, p.duracion, p.prioridad])

    def cargar_csv(self, archivo: str):
        from src.proceso import Proceso
        Proceso.limpiar_pids()
        self.procesos = {}
        with open(archivo, newline='') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                self.agregar(Proceso(row['pid'], int(row['duracion']), int(row['prioridad'])))
