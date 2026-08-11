from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from dataclasses import dataclass


class ZoneTypes(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class ZoneColors(Enum):
    GOLD = "gold"
    BLACK = "black"
    RED = "red"
    DARKRED = "darkred"
    PURPLE = "purple"
    BROWN = "brown"
    MAROON = "maroon"
    ORANGE = "orange"
    CRIMSON = "crimson"
    RAINBOW = "rainbow"
    WHITE = "white"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    GRAY = "gray"
    VIOLET = "violet"

# SUPPORTED_DISPLAY_COLORS = {
#     "red",
#     "green",
#     "blue",
#     "yellow",
#     "purple",
# }

# if hub.color in SUPPORTED_DISPLAY_COLORS:
#     gerçek renkle göster
# else:
#     default terminal rengiyle göster


class Hub(BaseModel):
    name: str
    x: int
    y: int
    zone: ZoneTypes = ZoneTypes.NORMAL
    color: str | None = None
    max_drones: int = Field(default=1, ge=1)


class Connection(BaseModel):
    hub_a: str
    hub_b: str
    max_link_capacity: int = Field(default=1, ge=1)


class MapConfig(BaseModel):
    """Validate and store map configuration values."""
    nb_drones: int = Field(ge=1)
    hubs: dict[str, Hub]
    connections: list[Connection]