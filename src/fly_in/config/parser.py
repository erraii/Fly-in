from pathlib import Path
from .model import MapConfig, Hub, Connection


class ConfigParser:
    """Parse a KEY: VALUE configuration file."""

    def __init__(self, path: str) -> None:
        self.path = path

    def parse(self) -> MapConfig:
        """Read the config file and return raw string values."""
        nb_drones: int | None = None
        start_hub: Hub | None = None
        end_hub: Hub | None = None
        hubs: dict[str, Hub] = {}
        connections: list[Connection] = []

        try:
            with Path(self.path).open("r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    line = line.strip()

                    if not line:
                        continue

                    if line.startswith("#"):
                        continue

                    key, value = self._parse_line(line, line_number)

                    match key:
                        case "nb_drones":
                            if nb_drones is not None:
                                raise ValueError("Duplicate nb_drones")
                            nb_drones = value.strip()

                        case "start_hub":
                            if start_hub is not None:
                                raise ValueError("Duplicate start_hub")
                            hub = self._parse_hub(value)
                            start_hub = hub
                            self._add_hub(hubs, hub)

                        case "hub":
                            hub = self._parse_hub(value)
                            self._add_hub(hubs, hub)

                        case "end_hub":
                            if end_hub is not None:
                                raise ValueError("Duplicate end_hub")
                            hub = self._parse_hub(value)
                            end_hub = hub
                            self._add_hub(hubs, hub)

                        case "connection":

                            if line.count("-") != 1:
                                raise ValueError(
                                    f"Invalid config syntax at line {line_number}: {line}"
                                )

                            hub1, hub2 = line.split("-", 1)
                            hub1 = hub1.strip()
                            hub2 = hub2.strip()

                        case _:  # Default case
                            raise ValueError(
                                f"Invalid key at line {line_number}: {line}"
                            )

        except Exception:
            raise FileNotFoundError(
                f"File '{self.path}' not found"
            )

        return MapConfig(
                nb_drones=nb_drones,
                hubs=hubs,
                connections=connections,
            )

    def _add_hub(self, hubs: dict[str, Hub], hub: Hub,) -> None:
        if hub.name in hubs:
            raise ValueError(
                f"Duplicate hub name: {hub.name}"
            )

        hubs[hub.name] = hub

    def _parse_options(self, options: str) -> dict[str, str]:
        if not options.startswith("[") or not options.endswith("]"):
            raise ValueError("Invalid options format")

        content = options[1:-1].strip()

        if not content:
            return {}

        result: dict[str, str] = {}

        for option in content.split():
            if option.count("=") != 1:
                raise ValueError(
                    f"Invalid option format: {option}"
                )

            key, value = option.split("=", 1)

            if not key or not value:
                raise ValueError(
                    f"Invalid option format: {option}"
                )

            if key in result:
                raise ValueError(
                    f"Duplicate option: {key}"
                )

            result[key] = value

            return result

    def _parse_hub(self, value: str) -> Hub:
        metadata: dict[str, str] = {}

        parts = value.split(maxsplit=3)
        if len(parts) == 3:
            name, x, y = parts
        elif len(parts) == 4:
            name, x, y, options = parts
            metadata = self._parse_options(options)
        else:
            raise ValueError("Invalid hub format")
        return Hub(
                name=name,
                x=x,
                y=y,
                **metadata,
            )

    def _parse_line(self, line: str, line_number: int) -> tuple[str, str]:
        """Parse a single KEY:VALUE line."""
        if line.count(":") != 1:
            raise ValueError(
                f"Invalid config syntax at line {line_number}: {line}"
            )

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError(f"Missing key at line {line_number}: {line}")

        if not value:
            raise ValueError(f"Missing value at line {line_number}: {line}")

        return key, value
