from .drone import Drone
from config import MapConfig


class HubState:
    def __init__(self) -> None:
        self.occupants: set[int] = set()


class ConnectionState:
    def __init__(self) -> None:
        self.occupants: set[int] = set()


class SimulationState:
    """Store the complete mutable state of the simulation."""

    def __init__(self, config: MapConfig, drones: list[Drone]) -> None:
        self.hubs: dict[str, HubState] = {
            hub_name: HubState()
            for hub_name in config.hubs
        }

        self.connections: dict[
            tuple[str, str],
            ConnectionState,
        ] = {}

        for connection in config.connections:
            key = self.connection_key(
                connection.hub_a,
                connection.hub_b,
            )
            self.connections[key] = ConnectionState()

        self.drones: dict[int, Drone] = {
            drone.id: drone
            for drone in drones
        }

        for drone in drones:
            self.hubs[config.start_hub].occupants.add(
                drone.id
            )

    @staticmethod
    def connection_key(hub_a: str, hub_b: str,) -> tuple[str, str]:
        if hub_a < hub_b:
            return hub_a, hub_b
        return hub_b, hub_a
