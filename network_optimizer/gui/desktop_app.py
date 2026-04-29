import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
import json
from tkinter import filedialog
from typing import List, Tuple

from network_optimizer.core.graph import NetworkGraph
from network_optimizer.core.algorithms import kruskal_mst, dijkstra, nearest_neighbor_tsp

class NetworkOptimizerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Network Route Optimization - Herramienta de Optimización de Rutas de Escaneo de Redes")
        self.graph = NetworkGraph()
        self._build_ui()
        self._load_demo_graph()
        self.draw_graph()

    def _build_ui(self):
        # Left frame: controls
        frm = ttk.Frame(self.root)
        frm.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)

        # Host input
        ttk.Label(frm, text="Host (nombre):").pack(anchor=tk.W)
        self.host_entry = ttk.Entry(frm)
        self.host_entry.pack(fill=tk.X)
        ttk.Button(frm, text="Agregar Host", command=self.add_host).pack(fill=tk.X, pady=2)

        ttk.Separator(frm).pack(fill=tk.X, pady=4)

        # Edge input
        ttk.Label(frm, text="Conexión (u,v,peso):").pack(anchor=tk.W)
        self.u_entry = ttk.Entry(frm)
        self.u_entry.pack(fill=tk.X)
        self.v_entry = ttk.Entry(frm)
        self.v_entry.pack(fill=tk.X)
        self.w_entry = ttk.Entry(frm)
        self.w_entry.pack(fill=tk.X)
        ttk.Button(frm, text="Agregar Conexión", command=self.add_edge).pack(fill=tk.X, pady=2)

        ttk.Separator(frm).pack(fill=tk.X, pady=4)

        # Dijkstra controls
        ttk.Label(frm, text="Dijkstra - Origen/Destino:").pack(anchor=tk.W)
        self.src_entry = ttk.Entry(frm)
        self.src_entry.pack(fill=tk.X)
        self.dst_entry = ttk.Entry(frm)
        self.dst_entry.pack(fill=tk.X)
        ttk.Button(frm, text="Calcular Dijkstra", command=self.run_dijkstra).pack(fill=tk.X, pady=2)

        ttk.Separator(frm).pack(fill=tk.X, pady=4)

        ttk.Button(frm, text="Calcular MST (Kruskal)", command=self.run_kruskal).pack(fill=tk.X, pady=2)
        ttk.Button(frm, text="Calcular Escaneo Hamiltoniano", command=self.run_hamiltonian).pack(fill=tk.X, pady=2)

        ttk.Separator(frm).pack(fill=tk.X, pady=4)

        ttk.Label(frm, text="Resultados:").pack(anchor=tk.W)
        self.result_text = tk.Text(frm, width=40, height=15)
        self.result_text.pack()

        ttk.Separator(frm).pack(fill=tk.X, pady=4)
        # Save / Load
        ttk.Button(frm, text="Guardar Grafo", command=self.save_graph).pack(fill=tk.X, pady=2)
        ttk.Button(frm, text="Cargar Grafo", command=self.load_graph).pack(fill=tk.X, pady=2)
        ttk.Button(frm, text="Guía de uso", command=self.show_guide).pack(fill=tk.X, pady=2)

        # Right frame: matplotlib canvas
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        plt.tight_layout()
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_host(self):
        host = self.host_entry.get().strip()
        if not host:
            messagebox.showerror("Entrada inválida", "Ingrese un nombre de host")
            return
        try:
            self.graph.add_host(host)
            self.draw_graph()
            self.result_text.insert(tk.END, f"Host '{host}' agregado.\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_edge(self):
        u = self.u_entry.get().strip()
        v = self.v_entry.get().strip()
        w = self.w_entry.get().strip()
        try:
            if not u or not v or not w:
                raise ValueError("Complete u, v y peso")
            weight = float(w)
            if weight < 0:
                raise ValueError("El peso debe ser no negativo")
            self.graph.add_edge(u, v, weight)
            self.draw_graph()
            self.result_text.insert(tk.END, f"Conexión {u} - {v} ({weight}) agregada.\n")
        except Exception as e:
            messagebox.showerror("Error al agregar arista", str(e))

    def run_kruskal(self):
        try:
            mst, total = kruskal_mst(self.graph)
            self.result_text.insert(tk.END, f"MST costo total: {total:.3f}\n")
            for u, v, w in mst:
                self.result_text.insert(tk.END, f"  {u} - {v}: {w}\n")
            self.draw_graph(highlight_mst=mst)
        except Exception as e:
            messagebox.showerror("Error MST", str(e))

    def run_dijkstra(self):
        src = self.src_entry.get().strip()
        dst = self.dst_entry.get().strip()
        try:
            if not src or not dst:
                raise ValueError("Ingrese origen y destino")
            path, cost = dijkstra(self.graph, src, dst)
            if not path:
                self.result_text.insert(tk.END, "No hay camino entre los nodos especificados.\n")
            else:
                self.result_text.insert(tk.END, f"Ruta Dijkstra {src} -> {dst} (costo {cost:.3f}):\n")
                self.result_text.insert(tk.END, "  " + " -> ".join(path) + "\n")
            self.draw_graph(highlight_path=path)
        except Exception as e:
            messagebox.showerror("Error Dijkstra", str(e))

    def run_hamiltonian(self):
        start = self.src_entry.get().strip() or None
        try:
            route, cost = nearest_neighbor_tsp(self.graph, start=start)
            if not route:
                self.result_text.insert(tk.END, "Grafo vacío: sin ruta Hamiltoniana.\n")
            else:
                self.result_text.insert(tk.END, f"Ruta Hamiltoniana (heurística) costo estimado {cost:.3f}:\n")
                self.result_text.insert(tk.END, "  " + " -> ".join(route) + "\n")
            self.draw_graph(highlight_path=route)
        except Exception as e:
            messagebox.showerror("Error Hamiltoniano", str(e))

    def _load_demo_graph(self):
        demo_nodes = ["A", "B", "C", "D", "E", "F"]
        demo_edges = [
            ("A", "B", 10),
            ("A", "C", 15),
            ("B", "D", 12),
            ("C", "E", 10),
            ("D", "E", 2),
            ("D", "F", 1),
            ("E", "F", 5),
            ("B", "C", 7),
        ]
        for n in demo_nodes:
            angle = 2 * math.pi * demo_nodes.index(n) / len(demo_nodes)
            pos = (0.5 + 0.35 * math.cos(angle), 0.5 + 0.35 * math.sin(angle))
            self.graph.add_host(n, pos=pos)
        for u, v, w in demo_edges:
            self.graph.add_edge(u, v, w)

    def save_graph(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if not path:
                return
            data = {
                "nodes": {n: list(self.graph.positions[n]) for n in self.graph.nodes()},
                "edges": [{"u": u, "v": v, "w": w} for (u, v, w) in self.graph.edges()],
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.result_text.insert(tk.END, f"Grafo guardado en: {path}\n")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def load_graph(self):
        try:
            path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
            if not path:
                return
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.graph = NetworkGraph()
            nodes = data.get("nodes", {})
            for n, pos in nodes.items():
                try:
                    self.graph.add_host(n, pos=tuple(pos))
                except Exception:
                    self.graph.add_host(n)
            for e in data.get("edges", []):
                u = e.get("u")
                v = e.get("v")
                w = e.get("w")
                if u is None or v is None or w is None:
                    continue
                try:
                    self.graph.add_edge(u, v, float(w))
                except Exception:
                    continue
            self.result_text.insert(tk.END, f"Grafo cargado desde: {path}\n")
            self.draw_graph()
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def draw_graph(self, highlight_mst: List[Tuple[str, str, float]] = None, highlight_path: List[str] = None):
        self.ax.clear()
        xs = [self.graph.positions[n][0] for n in self.graph.nodes()]
        ys = [self.graph.positions[n][1] for n in self.graph.nodes()]
        for u, v, w in self.graph.edges():
            x1, y1 = self.graph.positions[u]
            x2, y2 = self.graph.positions[v]
            self.ax.plot([x1, x2], [y1, y2], color="#cccccc", zorder=1)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.ax.text(mx, my, f"{w}", color="#777777", fontsize=8)

        if highlight_mst:
            for u, v, w in highlight_mst:
                x1, y1 = self.graph.positions[u]
                x2, y2 = self.graph.positions[v]
                self.ax.plot([x1, x2], [y1, y2], color="green", linewidth=2.5, zorder=3)

        if highlight_path and len(highlight_path) >= 2:
            path_pairs = list(zip(highlight_path[:-1], highlight_path[1:]))
            for u, v in path_pairs:
                if u in self.graph.positions and v in self.graph.positions:
                    x1, y1 = self.graph.positions[u]
                    x2, y2 = self.graph.positions[v]
                    self.ax.plot([x1, x2], [y1, y2], color="red", linewidth=2.5, zorder=4)
            start = highlight_path[0]
            end = highlight_path[-1]
            if start in self.graph.positions:
                x, y = self.graph.positions[start]
                self.ax.scatter([x], [y], color="blue", s=100, zorder=5)
                self.ax.text(x, y, f" {start}", color="blue")
            if end in self.graph.positions:
                x, y = self.graph.positions[end]
                self.ax.scatter([x], [y], color="orange", s=100, zorder=5)
                self.ax.text(x, y, f" {end}", color="orange")

        for n in self.graph.nodes():
            x, y = self.graph.positions[n]
            self.ax.scatter([x], [y], color="black", s=40, zorder=6)
            self.ax.text(x, y, f" {n}", verticalalignment="bottom")

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title("Network Graph")
        self.canvas.draw_idle()

    def show_guide(self):
        guide = tk.Toplevel(self.root)
        guide.title("Guía de uso - Network Optimizer")
        guide.geometry("600x500")
        txt = tk.Text(guide, wrap=tk.WORD)
        txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        steps = (
            "Guía de uso - Herramienta de Optimización de Rutas de Escaneo de Redes\n\n"
            "1) Exploración inicial:\n"
            "   - Al abrir la aplicación ya tienes un grafo de ejemplo cargado.\n"
            "   - Observa los nodos y las aristas con sus pesos (latencias en ms).\n\n"
            "2) Añadir hosts y conexiones:\n"
            "   - Escribe un nombre en 'Host (nombre)' y pulsa 'Agregar Host' para añadir un nuevo nodo.\n"
            "   - Para añadir una conexión, introduce 'u' (origen), 'v' (destino) y 'peso' (latencia) y pulsa 'Agregar Conexión'.\n\n"
            "3) Calcular MST (Kruskal):\n"
            "   - Pulsa 'Calcular MST (Kruskal)' para obtener el Árbol de Expansión Mínima.\n"
            "   - El MST se resaltará en verde y el coste total aparecerá en el panel de resultados.\n\n"
            "4) Calcular Dijkstra (ruta mínima):\n"
            "   - Introduce el nodo origen y destino en los campos correspondientes y pulsa 'Calcular Dijkstra'.\n"
            "   - La ruta óptima se resaltará en rojo; el origen se marca en azul y el destino en naranja.\n\n"
            "5) Calcular Escaneo Hamiltoniano (heurística):\n"
            "   - Pulsa 'Calcular Escaneo Hamiltoniano' para obtener una ruta que visita cada host una vez (heurística).\n"
            "   - La ruta propuesta se resaltará en rojo y su coste estimado se mostrará en el panel de resultados.\n\n"
            "6) Guardar/Cargar grafos:\n"
            "   - Usa 'Guardar Grafo' para exportar el grafo actual a un archivo JSON.\n"
            "   - Usa 'Cargar Grafo' para importar un grafo previamente guardado.\n\n"
            "7) Recomendaciones prácticas:\n"
            "   - Para gráficos complejos, ajusta las posiciones manualmente en el JSON antes de cargar si deseas una vista específica.\n"
            "   - Ten en cuenta que la heurística Hamiltoniana no garantiza optimalidad en todos los casos.\n\n"
            "8) Ejemplo rápido:\n"
            "   - Añade un host 'G', conecta 'G' con 'A' (5ms) y 'G' con 'F' (8ms).\n"
            "   - Ejecuta Dijkstra entre 'G' y 'E' para ver la ruta más eficiente.\n\n"
            "Si necesitas más funciones (exportar imagen, validación avanzada, tests), puedo implementarlas a petición."
        )
        txt.insert(tk.END, steps)
        txt.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = NetworkOptimizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
