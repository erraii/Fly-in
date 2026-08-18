import sys
from config import ConfigParser, ConfigParseError
from solver import Graph, DijkstraSolver
from simulation import Drone, SimulationState, Simulator


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 fly_in.py <map_file>")
        return

    map_path = sys.argv[1]

    try:
        map_config = ConfigParser(map_path).parse()
        # print(config)
    except (FileNotFoundError, ConfigParseError) as error:
        print(f"Error: {error}")
        return

    graph = Graph(map_config)
    graph.construct()
    dist_path = DijkstraSolver(graph).solve(map_config.start_hub)
    print(dist_path)

    drone_list: list[Drone] = []

    for i in range(1, map_config.nb_drones + 1):
        drone = Drone(i, map_config.start_hub)
        drone_list.append(drone)

    # states = SimulationState(map_config, drone_list)

    # simulator = Simulator(graph, map_config.nb_drones)
    # simulator.run()

    simulator = Simulator(
        map_config, graph, drone_list)

    # print("---------Hubs----------")
    # for hub, state in simulator.state.hubs.items():
    #     print(f"{hub}: {state.occupants}")
    # print("------Connections------")
    # for connection, drone_list in simulator.state.connections.items():
    #     print(f"{connection}: {drone_list.occupants}")

    # simulator.run_one_drone(1)
    simulator.run()

    # print("---------Hubs----------")

    # for hub, state in simulator.state.hubs.items():
    #     print(
    #         f"{hub}: {state.occupants}"
    #     )


if __name__ == "__main__":
    main()
