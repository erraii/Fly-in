from .drone import Drone
from config import MapConfig


class HubState:
    occupants: set[int]


class ConnectionState:
    occupants: set[int]


class SimulationState:
    """Store the complete mutable state of the simulation."""

    def __init__(
        self,
        config: MapConfig,
        drones: list[Drone],
    ) -> None:
        self.hubs: dict[str, HubState] = {
            hub_name: HubState() for hub_name in config.hubs
        }

        self.connections: dict[
            tuple[str, str], ConnectionState,
        ] = {}

        for connection in config.connections:
            key = self.connection_key(
                connection.hub_a, connection.hub_b,
            )

            self.connections[key] = ConnectionState()

        self.drones: dict[int, Drone] = {
            drone.drone_id: drone for drone in drones
        }
