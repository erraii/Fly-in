from math import inf
from .graph import Graph


class DijkstraSolver:
    """Find shortest paths in a weighted graph using Dijkstra's algorithm."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.cache: dict[
            str,
            dict[str, tuple[float, str | None]],
        ] = {}

    def solve(self, source: str) -> dict[str, tuple[float, str | None]]:
        """Calculate shortest distances and previous paths
        from source to every reachable hub."""

        if source in self.cache:
            return self.cache[source]

        unvisited = list(self.graph.graph.keys())

        dist_path: dict[str, tuple[float, str | None]] = {}

        for hub in self.graph.graph:
            if hub == source:
                dist_path[hub] = (0.0, None)
            else:
                dist_path[hub] = (float(inf), None)

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

        self.cache[source] = dist_path
        return dist_path

    def get_path(
        self,
        source: str,
        destination: str,
    ) -> list[str]:
        """Return shortest path from source to destination."""
        dist_path = self.solve(source)

        if destination not in dist_path:
            return []

        if dist_path[destination][0] == inf:
            return []

        path: list[str] = []
        current: str | None = destination

        while current is not None:
            path.append(current)
            current = dist_path[current][1]

        path.reverse()
        return path
