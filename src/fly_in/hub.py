from .coordinate import Coordinate
from enum import Enum
from dataclasses import dataclass








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


        