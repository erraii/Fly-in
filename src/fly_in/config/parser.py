from pathlib import Path
from typing import TypedDict, NotRequired


class Hub(TypedDict):
    name: str
    x: int
    y: int
    type: NotRequired[list[str]]

class Connection(TypedDict):
    connection: str

class ConfigParser:
    """Parse a KEY: VALUE configuration file."""

    def __init__(self, path: str) -> None:
        self.path = path

    def parse(self) -> dict[str, Hub | Connection | int]:
        