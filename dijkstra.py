from typing import Dict, List, Tuple, Optional
import heapq

Node = str
Weight = float
Edge_to = Tuple[Node, Weight]
AdjacencyList = Dict[Node, List[Edge_to]]


def check_graph(graph: AdjacencyList) -> None:
    for node in graph:
        for node_to, weight in graph[node]:
            if not node_to in graph:
                err = f"Invalid graph: node '{node}' links to a non-existent node '{node_to}'"
                raise ValueError(err)
            if weight < 0:
                err = f"Invalid graph: negative weight {weight} in edge from '{node}' to '{node_to}'"
                raise ValueError(err)


def dijkstra(graph: AdjacencyList, source: Node) -> Tuple[Dict[Node, Weight], Dict[Node, Optional[Node]]]:
    """
    Algoritmo de Dijkstra para distancias mínimas en un grafo usando listas de adyacencia.
    Retorna:
      - distances: distancia mínima desde source a cada nodo
      - previous: predecesor para reconstruir caminos
    """
    if source not in graph:
        raise KeyError(f"El nodo origen {source!r} no existe en el grafo.")

    distances: Dict[Node, float] = {node: float("inf") for node in graph}
    distances[source] = 0.0
    previous: Dict[Node, Optional[Node]] = {node: None for node in graph}

    priority_queue: List[Tuple[float, Node]] = [(0.0, source)]

    while priority_queue:
        current_distance, node = heapq.heappop(priority_queue)

        # Ignorar entradas obsoletas
        if current_distance > distances[node]:
            continue

        for node_to, weight in graph[node]:
            new_distance = current_distance + weight
            if new_distance < distances[node_to]:
                distances[node_to] = new_distance
                previous[node_to] = node
                heapq.heappush(priority_queue, (new_distance, node_to))

    return distances, previous


def reconstruct_path(previous: Dict[Node, Optional[Node]], source: Node, target: Node) -> List[Node]:
    """
    Reconstruye el camino desde source hasta target.
    Si no existe camino, retorna [].
    """
    path: List[Node] = []
    current: Optional[Node] = target

    while current is not None:
        path.append(current)
        current = previous.get(current)

    path.reverse()
    return path if path and path[0] == source else []


def show_path(distances, previous, source, target):
    path = reconstruct_path(previous, source, target)
    print(f"Distancia mínima {source} -> {target}: {distances[target]:6.1f}   Camino: {path}")


if __name__ == "__main__":
    graph: AdjacencyList = {
        "A": [("B", 10.0), ("C", 5.0)],
        "B": [("D", 1.0)],
        "C": [("B", 4.0), ("D", 3.0)],
        "D": [("A", 6.0), ("E", 2.0), ("F", 4.0)],
        "E": [("F", 1.0)],
        "F": [("B", 7.0), ("G", 2.0)],
        "G": [("F", 3.0)],
        "H": []
    }

    check_graph(graph)
    source = "G"
    distances, previous = dijkstra(graph, source)
    for target in graph:
        show_path(distances, previous, source, target)
