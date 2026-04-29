import math
import heapq
from typing import Dict, Tuple, List, Any, Set
from network_optimizer.core.graph import NetworkGraph

def kruskal_mst(graph: NetworkGraph) -> Tuple[List[Tuple[str, str, float]], float]:
    """Implementación de Kruskal que retorna las aristas del MST y el costo total."""
    parent = {}
    rank = {}

    def make_set(x):
        parent[x] = x
        rank[x] = 0

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        else:
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1
        return True

    for node in graph.nodes():
        make_set(node)

    edges = sorted(graph.edges(), key=lambda e: e[2])
    mst = []
    total = 0.0
    for u, v, w in edges:
        if union(u, v):
            mst.append((u, v, w))
            total += w
    return mst, total


def dijkstra(graph: NetworkGraph, source: str, target: str) -> Tuple[List[str], float]:
    """Dijkstra clásico para caminos de menor costo (pesos no negativos).

    Retorna la lista de nodos desde source hasta target y el costo total.
    """
    if source not in graph.adj or target not in graph.adj:
        raise KeyError("Source o target no existe en el grafo")

    dist = {node: math.inf for node in graph.nodes()}
    prev: Dict[str, Any] = {node: None for node in graph.nodes()}
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == target:
            break
        for v, w in graph.neighbors(u).items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    if dist[target] == math.inf:
        return [], math.inf

    # reconstruct path
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path, dist[target]


def nearest_neighbor_tsp(graph: NetworkGraph, start: str = None) -> Tuple[List[str], float]:
    """Heurística del vecino más cercano para una ruta Hamiltoniana aproximada.

    No garantiza optimalidad; devuelve ruta (sin cerrar en ciclo) y costo total.
    """
    nodes = graph.nodes()
    if not nodes:
        return [], 0.0
    unvisited: Set[str] = set(nodes)
    if start is None or start not in unvisited:
        start = nodes[0]
    route = [start]
    unvisited.remove(start)
    total = 0.0
    current = start

    while unvisited:
        # find nearest neighbor among unvisited that is reachable
        neighs = graph.neighbors(current)
        candidate = None
        best = math.inf
        for v in unvisited:
            w = neighs.get(v, math.inf)
            if w < best:
                best = w
                candidate = v
        if candidate is None:
            # disconnected: pick arbitrary unvisited and add a large penalty (simulate reconnect)
            candidate = next(iter(unvisited))
            # best remains inf => treat as unreachable; use shortest path cost via Dijkstra if exists
            try:
                path, cost = dijkstra(graph, current, candidate)
            except KeyError:
                cost = math.inf
            if cost == math.inf:
                # no path: give very large cost
                cost = 1e6
            total += cost
            # append only the endpoint to simulate visiting; this is heuristic fallback
            route.append(candidate)
            unvisited.remove(candidate)
            current = candidate
            continue

        total += best
        route.append(candidate)
        unvisited.remove(candidate)
        current = candidate

    return route, total
