from dataclasses import dataclass


@dataclass
class Coordinate:
    """Class for the 2 axis coordinate system"""
    x: int
    y: int

    def get_coordinate(self) -> tuple[int, int]:
        return (self.x, self.y)
