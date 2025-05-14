class Proceso:
    _pids_existentes = set()

    def __init__(self, pid: str, duracion: int, prioridad: int):
        if not pid:
            raise ValueError("PID no puede estar vacío.")
        if pid in Proceso._pids_existentes:
            raise ValueError(f"PID duplicado: {pid}")
        if duracion <= 0:
            raise ValueError("Duración debe ser positiva.")
        if not isinstance(prioridad, int):
            raise ValueError("Prioridad debe ser un entero.")

        self.pid = pid
        self.duracion = duracion
        self.prioridad = prioridad
        self.tiempo_restante = duracion
        self.tiempo_llegada = 0
        self.tiempo_inicio = None
        self.tiempo_fin = None

        Proceso._pids_existentes.add(pid)

    @classmethod
    def limpiar_pids(cls):
        cls._pids_existentes.clear()
