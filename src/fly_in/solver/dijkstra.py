from math import inf
from .graph import Graph


class DijkstraSolver:
    """Find shortest paths in a weighted graph using Dijkstra's algorithm."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def solve(self, source: str) -> dict[str, tuple[float, str]]:
        """Calculate shortest distances and previous paths
        from source to every reachable hub."""

        unvisited = list(self.graph.graph.keys())

        dist_path: dict[str, tuple[float, str | None]] = {}

        for hub in self.graph.graph:
            if hub == source:
                dist_path[hub] = (0.0, None)
            else:
                dist_path[hub] = (float("inf"), None)

        while unvisited:
            current = min(
                unvisited,
                key=lambda hub: dist_path[hub][0],
            )

            for neighbor in self.graph.graph[current]:
                new_distance = (
                    dist_path[current][0]
                    + self.graph.get_cost(neighbor)
                )

                if new_distance < dist_path[neighbor][0]:
                    dist_path[neighbor] = new_distance, current

            unvisited.remove(current)

        return dist_path
