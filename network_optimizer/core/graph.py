import random
from typing import Dict, Tuple, List

class NetworkGraph:
    """Clase que representa una red como grafo no dirigido con pesos.

    Vértices: dict de host -> pos (x,y) para visualización
    Aristas: dict con claves (u,v) (u<v) -> peso
    """

    def __init__(self):
        self.positions: Dict[str, Tuple[float, float]] = {}
        # store adjacency as dict: node -> dict(neighbor->weight)
        self.adj: Dict[str, Dict[str, float]] = {}

    def add_host(self, host: str, pos: Tuple[float, float] = None):
        if host in self.adj:
            return
        self.adj[host] = {}
        if pos is None:
            # random position for visualization
            pos = (random.uniform(0, 1), random.uniform(0, 1))
        self.positions[host] = pos

    def add_edge(self, u: str, v: str, weight: float):
        if u == v:
            raise ValueError("No se permiten bucles (u != v)")
        for node in (u, v):
            if node not in self.adj:
                self.add_host(node)
        # undirected: store both ways
        self.adj[u][v] = weight
        self.adj[v][u] = weight

    def nodes(self) -> List[str]:
        return list(self.adj.keys())

    def edges(self) -> List[Tuple[str, str, float]]:
        seen = set()
        out = []
        for u in self.adj:
            for v, w in self.adj[u].items():
                if (v, u) in seen:
                    continue
                seen.add((u, v))
                out.append((u, v, w))
        return out

    def neighbors(self, u: str) -> Dict[str, float]:
        return self.adj.get(u, {})
