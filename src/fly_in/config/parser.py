from pathlib import Path
from .model import MapConfig, Hub, Connection


class ConfigParseError(Exception):
    """Error raised when parsing a map file."""


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
        seen_connections: set[tuple[str, str]] = set()

        try:
            with Path(self.path).open("r", encoding="utf-8") as file:

                for line_number, line in enumerate(file, start=1):
                    line = line.split("#", 1)[0].strip()

                    if not line:
                        continue

                    try:
                        key, value = self._parse_line(line)

                        if nb_drones is None and key != "nb_drones":
                            raise ValueError(
                                "First configuration entry must be nb_drones"
                            )

                        match key:
                            case "nb_drones":
                                if nb_drones is not None:
                                    raise ValueError("Duplicate nb_drones")
                                nb_drones = int(value)

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

                                connection = self._parse_connection(value)

                                if connection.hub_a not in hubs:
                                    raise ValueError(
                                        f"Undefined hub: {connection.hub_a}",
                                    )

                                if connection.hub_b not in hubs:
                                    raise ValueError(
                                        f"Undefined hub: {connection.hub_b}",
                                    )

                                connection_key = tuple(
                                    sorted((connection.hub_a,
                                            connection.hub_b))
                                )

                                if connection_key in seen_connections:
                                    raise ValueError(
                                        f"Duplicate connection: "
                                        f"{connection.hub_a}-"
                                        f"{connection.hub_b}"
                                    )

                                seen_connections.add(connection_key)
                                connections.append(connection)

                            case _:  # Default case
                                raise ValueError(
                                    f"Invalid key at line "
                                    f"{line_number}: {line}"
                                )

                    except ValueError as error:
                        raise ConfigParseError(
                            f"Invalid config at line "
                            f"{line_number}: {line}\n"
                            f"Reason: {error}"
                        ) from error

        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"File '{self.path}' not found"
            ) from error

        if nb_drones is None:
            raise ConfigParseError("Missing nb_drones")

        if start_hub is None:
            raise ConfigParseError("Missing start_hub")

        if end_hub is None:
            raise ConfigParseError("Missing end_hub")

        return MapConfig.model_validate({
                "nb_drones": nb_drones,
                "start_hub": start_hub.name,
                "end_hub": end_hub.name,
                "hubs": hubs,
                "connections": connections,
            })

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

    def _parse_connection(self, value: str) -> Connection:
        metadata: dict[str, str] = {}

        parts = value.split(maxsplit=1)
        connection = parts[0]
        if connection.count("-") != 1:
            raise ValueError("Invalid connection format")
        hub_a, hub_b = connection.split("-", 1)
        # print(f"hub a: {hub_a}, hub b: {hub_b}")
        if len(parts) == 2:
            options = parts[1]
            metadata = self._parse_options(options)

        return Connection(
                hub_a=hub_a,
                hub_b=hub_b,
                **metadata,
            )

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

    def _parse_line(self, line: str) -> tuple[str, str]:
        """Parse a single KEY:VALUE line."""
        if line.count(":") != 1:
            raise ValueError("Invalid config syntax")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError("Missing key")

        if not value:
            raise ValueError("Missing value")

        return key, value
