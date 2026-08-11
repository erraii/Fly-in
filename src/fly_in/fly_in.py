import sys
from pydantic import ValidationError
from config import ConfigParser


def main() -> None:
    #   Eray Input
    #   settings = load_settings("settings.json")
    """Load configuration and run the application."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        raw_settings = ConfigParser(sys.argv[1]).parse()
        # map_config = .model_validate(raw_settings)

    except FileNotFoundError as err:
        print(f"File error: {err}")
        return

    except ValidationError as err:
        print(f"Config validation error:\n{err}")
        return

    except ValueError as err:
        print(f"Config parser error: {err}")
        return

    # app = MazeApplication(settings)
    # app.run()


if __name__ == "__main__":
    main()
