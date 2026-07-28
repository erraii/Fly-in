from .coordinate import Coordinate
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


@dataclass
class Metadata:
    zone_type: ZoneTypes
    color: ZoneColors
    max_drones: int


class Zone:
    def __init__(self,
                 name: str,
                 coordinate: Coordinate,
                 metadata: Metadata,
                 ):
        self.name = name
        self.x = coordinate.x
        self.y = coordinate.y
        self.type = metadata.zone_type
        self.color = metadata.color
        self.capacity = metadata.max_drones


        