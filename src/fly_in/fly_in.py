import sys
from config import ConfigParser, ConfigParseError
from solver import Graph, DijkstraSolver


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 fly_in.py <map_file>")
        return

    map_path = sys.argv[1]

    try:
        config = ConfigParser(map_path).parse()
        # print(config)
    except (FileNotFoundError, ConfigParseError) as error:
        print(f"Error: {error}")
        return

    # Sonraki aşama:
    # graph = Graph(config)
    graph = Graph(config)
    graph.construct()
    distances = DijkstraSolver(graph).solve(config.start_hub)
    print(distances)
    
    # simulator = Simulator(graph, config.nb_drones)
    # simulator.run()


if __name__ == "__main__":
    main()
