from pydantic import BaseModel, ConfigDict, Field, field_validator
from enum import Enum


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


class Hub(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    x: int
    y: int

    zone: ZoneTypes = ZoneTypes.NORMAL
    color: str = Field(default="white", min_length=1)
    max_drones: int = Field(default=1, ge=1)

    @field_validator("color", mode="after")
    @classmethod
    def validate_color(cls, color: str) -> str:
        supported_colors = {
            zone_color.value
            for zone_color in ZoneColors
        }

        if color not in supported_colors:
            print(color)
            return ZoneColors.WHITE.value

        return color


class Connection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hub_a: str = Field(min_length=1)
    hub_b: str = Field(min_length=1)
    max_link_capacity: int = Field(default=1, ge=1)


class MapConfig(BaseModel):
    """Validate and store map configuration values."""
    nb_drones: int = Field(ge=1)
    start_hub: str
    end_hub: str
    hubs: dict[str, Hub]
    connections: list[Connection]
