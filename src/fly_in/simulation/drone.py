from enum import Enum


class DroneStatus(Enum):
    AT_HUB = "at_hub"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"


class Drone:
    def __init__(self, drone_id: int, start_hub: str) -> None:
        self.id = drone_id
        self.status = DroneStatus.AT_HUB
        self.current_hub: str | None = start_hub
        self.current_connection: tuple[str, str] | None = None
        self.destination_hub: str | None = None
        self.turns_remaining = 0
