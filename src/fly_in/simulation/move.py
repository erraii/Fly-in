from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    """Represent a planned movement for one drone."""

    drone_id: int
    destination: str
