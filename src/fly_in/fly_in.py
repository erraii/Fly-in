import sys
from config import ConfigParser, ConfigParseError
from solver import Graph, DijkstraSolver
from simulation import Drone


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
    dist_path = DijkstraSolver(graph).solve(config.start_hub)
    print(dist_path)

    drone_list: list[Drone] = []

    for i in range(1, config.nb_drones + 1):
        drone = Drone(i, config.start_hub)
        drone_list.append(drone)

    for drone in drone_list:
        print(drone.current_hub)

    # simulator = Simulator(graph, config.nb_drones)
    # simulator.run()


if __name__ == "__main__":
    main()
