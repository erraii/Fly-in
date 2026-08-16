from config import MapConfig, ZoneTypes


class Graph:
    """Construct a graph from a MapConfig."""

    def __init__(self, map_config: MapConfig) -> None:
        self.map_config = map_config
        self.graph: dict[str, list[str]] = {}

    def construct(self) -> None:
        for connection in self.map_config.connections:
            hub_a = self.map_config.hubs[connection.hub_a]
            hub_b = self.map_config.hubs[connection.hub_b]

            if hub_a.zone == ZoneTypes.BLOCKED:
                continue

            if hub_b.zone == ZoneTypes.BLOCKED:
                continue

            self.graph.setdefault(hub_a.name, []).append(hub_b.name)
            self.graph.setdefault(hub_b.name, []).append(hub_a.name)

        # for hub_name, neighbors in self.graph.items():
        #     print(
        #         f"hub: {hub_name} "
        #         f"cost: {self.get_cost(hub_name)} "
        #         f"neighbors: {neighbors}"
        #     )

    def get_neighbors(self, hub_name: str) -> list[str]:
        return self.graph.get(hub_name, [])

    def get_cost(self, hub_name: str) -> int:
        hub = self.map_config.hubs[hub_name]

        if hub.zone == ZoneTypes.RESTRICTED:
            return 2

        return 1
