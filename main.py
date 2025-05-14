import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler
from src.repositorio import RepositorioProcesos
from src.metrics import calcular_metricas


class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador de Procesos")
        self.repo = RepositorioProcesos()
        self.scheduler = FCFSScheduler()

        # Crear botones
        tk.Button(root, text="Agregar Proceso", command=self.agregar_proceso).pack(fill="x")
        tk.Button(root, text="Listar Procesos", command=self.listar_procesos).pack(fill="x")
        tk.Button(root, text="Eliminar Proceso", command=self.eliminar_proceso).pack(fill="x")
        tk.Button(root, text="Seleccionar Algoritmo", command=self.seleccionar_algoritmo).pack(fill="x")
        tk.Button(root, text="Ejecutar Planificación", command=self.ejecutar_planificacion).pack(fill="x")
        tk.Button(root, text="Guardar Procesos", command=self.guardar_procesos).pack(fill="x")
        tk.Button(root, text="Cargar Procesos", command=self.cargar_procesos).pack(fill="x")
        tk.Button(root, text="Salir", command=root.quit).pack(fill="x")

        # Área de texto para mostrar resultados
        self.resultado_text = tk.Text(root, height=15, width=80)
        self.resultado_text.pack(padx=10, pady=10)

    def agregar_proceso(self):
        pid = simpledialog.askstring("PID", "Ingrese el PID:")
        if not pid:
            return
        try:
            duracion = int(simpledialog.askstring("Duración", "Ingrese la duración:"))
            prioridad = int(simpledialog.askstring("Prioridad", "Ingrese la prioridad:"))
            self.repo.agregar(Proceso(pid, duracion, prioridad))
            messagebox.showinfo("Éxito", "Proceso agregado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def listar_procesos(self):
        # Limpiar área de resultados
        self.resultado_text.delete(1.0, tk.END)

        procesos = self.repo.listar()
        if not procesos:
            self.resultado_text.insert(tk.END, "No hay procesos registrados.\n")
        else:
            texto = "\n".join(f"{p.pid} | Duración: {p.duracion} | Prioridad: {p.prioridad}" for p in procesos)
            self.resultado_text.insert(tk.END, texto + "\n")

    def eliminar_proceso(self):
        pid = simpledialog.askstring("Eliminar Proceso", "Ingrese el PID a eliminar:")
        if pid:
            try:
                self.repo.eliminar(pid)
                messagebox.showinfo("Éxito", f"Proceso {pid} eliminado.")
            except KeyError:
                messagebox.showerror("Error", "No existe un proceso con ese PID.")

    def seleccionar_algoritmo(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar algoritmo")

        def set_fcfs():
            self.scheduler = FCFSScheduler()
            ventana.destroy()
            messagebox.showinfo("Algoritmo", "FCFS seleccionado.")

        def set_rr():
            q = simpledialog.askinteger("Quantum", "Ingrese el quantum:", minvalue=1)
            if q:
                self.scheduler = RoundRobinScheduler(quantum=q)
                ventana.destroy()
                messagebox.showinfo("Algoritmo", f"Round-Robin (q={q}) seleccionado.")

        tk.Button(ventana, text="FCFS", command=set_fcfs).pack(fill="x")
        tk.Button(ventana, text="Round-Robin", command=set_rr).pack(fill="x")

    def ejecutar_planificacion(self):
        if not self.scheduler:
            messagebox.showwarning("Advertencia", "Primero debes seleccionar un algoritmo.")
            return

        procesos = self.repo.listar()
        if not procesos:
            messagebox.showwarning("Advertencia", "No hay procesos para planificar.")
            return

        gantt = self.scheduler.planificar(procesos)
        metricas = calcular_metricas(procesos)

        # Limpiar área de resultados
        self.resultado_text.delete(1.0, tk.END)

        # Mostrar diagrama de Gantt
        self.resultado_text.insert(tk.END, "--- Diagrama de Gantt ---\n")
        for pid, inicio, fin in gantt:
            self.resultado_text.insert(tk.END, f"{pid}: {inicio} -> {fin}\n")

        # Mostrar métricas
        self.resultado_text.insert(tk.END, "\n--- Métricas ---\n")
        for k, v in metricas.items():
            self.resultado_text.insert(tk.END, f"{k}: {v:.2f}\n")

    def guardar_procesos(self):
        tipo = simpledialog.askstring("Formato", "Ingrese el formato (json/csv):")
        if tipo not in ("json", "csv"):
            messagebox.showerror("Error", "Formato no válido.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=f".{tipo}")
        if not ruta:
            return
        try:
            if tipo == "json":
                self.repo.guardar_json(ruta)
            else:
                self.repo.guardar_csv(ruta)
            messagebox.showinfo("Guardado", f"Procesos guardados en {ruta}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_procesos(self):
        tipo = simpledialog.askstring("Formato", "Ingrese el formato (json/csv):")
        if tipo not in ("json", "csv"):
            messagebox.showerror("Error", "Formato no válido.")
            return
        ruta = filedialog.askopenfilename(filetypes=[(tipo.upper(), f"*.{tipo}")])
        if not ruta:
            return
        try:
            if tipo == "json":
                self.repo.cargar_json(ruta)
            else:
                self.repo.cargar_csv(ruta)
            messagebox.showinfo("Cargado", f"Procesos cargados desde {ruta}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
