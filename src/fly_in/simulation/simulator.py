from config import Connection, MapConfig, ZoneTypes
from solver import DijkstraSolver, Graph
from .drone import Drone, DroneStatus
from .move import Move
from .state import SimulationState


class Simulator:
    def __init__(
        self,
        config: MapConfig,
        graph: Graph,
        drones: list[Drone],
    ) -> None:
        self.config = config
        self.graph = graph
        self.drones = drones
        self.state = SimulationState(config, drones)
        self.solver = DijkstraSolver(graph)
        self.turn = 0

        self.connections: dict[
            tuple[str, str],
            Connection,
        ] = {}

        self.connection_reservations: dict[
            tuple[str, str],
            int,
        ] = {}

        self.connection_outgoing: dict[
            tuple[str, str],
            int,
        ] = {}

        self.hub_incoming: dict[str, int] = {}
        self.hub_outgoing: dict[str, int] = {}

        self.next_hub_incoming: dict[str, int] = {}

        for connection in config.connections:
            key = self.state.connection_key(
                connection.hub_a,
                connection.hub_b,
            )
            self.connections[key] = connection

    def run_one_drone(self, drone_id: int) -> None:
        """Move one drone from start to end."""
        drone = self.state.drones[drone_id]

        path = self.solver.get_path(
            self.config.start_hub,
            self.config.end_hub,
        )

        if not path:
            raise ValueError("No path from start to end")

        for destination in path[1:]:
            move = Move(
                drone_id=drone.id,
                destination=destination,
            )

            if not self._can_move(drone, destination):
                raise RuntimeError(
                    f"D{drone.id} cannot move to {destination}"
                )

            self._commit(move)

            if drone.status == DroneStatus.IN_TRANSIT:
                self._finish_transit(drone)

    def _can_move(
        self,
        drone: Drone,
        destination: str,
    ) -> bool:
        """Check whether a drone can start moving to destination."""

        if drone.current_hub is None:
            return False

        source = drone.current_hub

        connection_key = self.state.connection_key(
            source,
            destination,
        )

        if connection_key not in self.connections:
            return False

        connection = self.connections[connection_key]
        connection_state = self.state.connections[connection_key]

        current_connection_usage = len(
            connection_state.occupants
        )

        outgoing_connection_usage = (
            self.connection_outgoing.get(
                connection_key,
                0,
            )
        )

        reserved_connection_usage = (
            self.connection_reservations.get(
                connection_key,
                0,
            )
        )

        projected_connection_usage = (
            current_connection_usage
            - outgoing_connection_usage
            + reserved_connection_usage
        )

        if (
            projected_connection_usage
            >= connection.max_link_capacity
        ):
            return False

        destination_hub = self.config.hubs[destination]

        if destination_hub.zone == ZoneTypes.BLOCKED:
            return False

        if destination == self.config.end_hub:
            return True

        if destination_hub.zone == ZoneTypes.RESTRICTED:
            future_incoming = self.next_hub_incoming.get(
                destination,
                0,
            )

            return (
                future_incoming
                < destination_hub.max_drones
            )

        current_occupants = len(
            self.state.hubs[destination].occupants
        )

        outgoing = self.hub_outgoing.get(
            destination,
            0,
        )

        incoming = self.hub_incoming.get(
            destination,
            0,
        )

        projected_occupancy = (
            current_occupants
            - outgoing
            + incoming
        )

        return (
            projected_occupancy
            < destination_hub.max_drones
        )

    def _commit_transit(
        self,
        drone: Drone,
        destination: str,
    ) -> None:
        if drone.current_connection is None:
            raise RuntimeError(
                f"D{drone.id} is in transit without a connection"
            )

        key = self.state.connection_key(
            drone.current_connection[0],
            drone.current_connection[1],
        )

        self.state.connections[key].occupants.remove(
            drone.id
        )

        self.state.hubs[destination].occupants.add(
            drone.id
        )

        drone.current_hub = destination
        drone.current_connection = None
        drone.destination_hub = None
        drone.turns_remaining = 0

        if destination == self.config.end_hub:
            drone.status = DroneStatus.DELIVERED
        else:
            drone.status = DroneStatus.AT_HUB

    def _commit(self, move: Move) -> None:
        drone = self.state.drones[move.drone_id]

        if drone.status == DroneStatus.IN_TRANSIT:
            self._commit_transit(drone, move.destination)
            return

        if drone.current_hub is None:
            raise RuntimeError("Drone is not at a hub")

        source = drone.current_hub
        destination = move.destination
        destination_hub = self.config.hubs[destination]

        self.state.hubs[source].occupants.remove(drone.id)

        if destination_hub.zone == ZoneTypes.RESTRICTED:
            key = self.state.connection_key(
                source,
                destination,
            )

            self.state.connections[key].occupants.add(drone.id)

            drone.status = DroneStatus.IN_TRANSIT
            drone.current_hub = None
            drone.current_connection = (
                source,
                destination,
            )
            drone.destination_hub = destination
            drone.turns_remaining = 1
            return

        self.state.hubs[destination].occupants.add(drone.id)

        drone.current_hub = destination

        if destination == self.config.end_hub:
            drone.status = DroneStatus.DELIVERED
        else:
            drone.status = DroneStatus.AT_HUB

    def _enter_connection(self, drone: Drone, source: str,
                          destination: str) -> None:
        key = self.state.connection_key(
            source, destination)

        self.state.connections[key].occupants.add(
            drone.id
        )

        drone.status = DroneStatus.IN_TRANSIT
        drone.current_hub = None
        drone.current_connection = (
            source, destination)
        drone.destination_hub = destination
        drone.turns_remaining = 1

        print(
            f"Turn {self.turn}: "
            f"D{drone.id}-{source}-{destination}"
        )

    def _finish_transit(
        self,
        drone: Drone,
    ) -> None:
        if drone.current_connection is None:
            raise RuntimeError(
                "In-transit drone has no connection"
            )

        if drone.destination_hub is None:
            raise RuntimeError(
                "In-transit drone has no destination"
            )

        source, destination = drone.current_connection

        key = self.state.connection_key(
            source,
            destination,
        )

        self.turn += 1

        self.state.connections[key].occupants.remove(
            drone.id
        )

        self._arrive_at_hub(
            drone,
            destination,
        )

        print(
            f"Turn {self.turn}: "
            f"D{drone.id}-{destination}"
        )

    def _arrive_at_hub(
        self,
        drone: Drone,
        destination: str,
    ) -> None:
        self.state.hubs[destination].occupants.add(
            drone.id
        )

        drone.current_hub = destination
        drone.current_connection = None
        drone.destination_hub = None
        drone.turns_remaining = 0

        if destination == self.config.end_hub:
            drone.status = DroneStatus.DELIVERED
        else:
            drone.status = DroneStatus.AT_HUB

    def _all_delivered(self) -> bool:
        return all(
            drone.status == DroneStatus.DELIVERED
            for drone in self.drones
        )

    def run(self) -> None:
        while not self._all_delivered():
            moved = self._run_turn()

            if not moved:
                print(f"\nDEADLOCK AT TURN {self.turn}")

                for drone in self.state.drones.values():
                    print(
                        f"D{drone.id}: "
                        f"status={drone.status}, "
                        f"hub={drone.current_hub}, "
                        f"connection={drone.current_connection}, "
                        f"destination={drone.destination_hub}"
                    )

                print("Hub incoming:", self.hub_incoming)
                print("Hub outgoing:", self.hub_outgoing)
                print(
                    "Next incoming:",
                    self.next_hub_incoming,
                )
                print(
                    "Connection reservations:",
                    self.connection_reservations,
                )

                raise RuntimeError(
                    "Simulation deadlock: no drone can move"
                )

    def _run_turn(self) -> bool:
        planned_moves: list[Move] = []

        self.connection_reservations.clear()
        self.connection_outgoing.clear()

        self.hub_incoming.clear()
        self.hub_outgoing.clear()
        self.next_hub_incoming.clear()

        # 1. Forced movements first
        for drone in self.state.drones.values():
            if drone.status != DroneStatus.IN_TRANSIT:
                continue

            move = self._plan_move(drone)

            if move is not None:
                self._reserve_move(drone, move)
                planned_moves.append(move)

        # 2. Normal movements
        for drone in self.state.drones.values():
            if drone.status != DroneStatus.AT_HUB:
                continue

            move = self._plan_move(drone)

            if move is not None:
                self._reserve_move(drone, move)
                planned_moves.append(move)

        if not planned_moves:
            return False

        for move in planned_moves:
            print(f"turn: {self.turn}, moves: {move}")
            self._commit(move)

        self.turn += 1
        return True

    def _plan_move(self, drone: Drone) -> Move | None:
        if drone.status == DroneStatus.DELIVERED:
            return None

        if drone.status == DroneStatus.IN_TRANSIT:
            if drone.destination_hub is None:
                raise RuntimeError(
                    f"D{drone.id} is in transit without a destination"
                )

            return Move(
                drone_id=drone.id,
                destination=drone.destination_hub,
            )

        if drone.current_hub is None:
            raise RuntimeError(
                f"D{drone.id} has no current hub"
            )

        best_destination: str | None = None
        best_cost = float("inf")

        for neighbor in self.graph.get_neighbors(
            drone.current_hub
        ):
            if not self._can_move(drone, neighbor):
                continue

            dist_path = self.solver.solve(neighbor)

            if self.config.end_hub not in dist_path:
                continue

            cost_to_goal = dist_path[
                self.config.end_hub
            ][0]

            if cost_to_goal < best_cost:
                best_cost = cost_to_goal
                best_destination = neighbor

        if best_destination is None:
            return None

        return Move(
            drone_id=drone.id,
            destination=best_destination,
        )

    def _reserve_move(
        self,
        drone: Drone,
        move: Move,
    ) -> None:
        """Reserve resources required by a planned move."""

        destination = move.destination

        if drone.status == DroneStatus.IN_TRANSIT:
            if drone.current_connection is None:
                raise RuntimeError(
                    f"D{drone.id} has no current connection"
                )

            connection_key = self.state.connection_key(
                drone.current_connection[0],
                drone.current_connection[1],
            )

            self.connection_outgoing[connection_key] = (
                self.connection_outgoing.get(
                    connection_key,
                    0,
                ) + 1
            )

            self.hub_incoming[destination] = (
                self.hub_incoming.get(
                    destination,
                    0,
                ) + 1
            )

            return

        if drone.current_hub is None:
            raise RuntimeError(
                f"D{drone.id} has no current hub"
            )

        source = drone.current_hub

        connection_key = self.state.connection_key(
            source,
            destination,
        )

        self.connection_reservations[connection_key] = (
            self.connection_reservations.get(connection_key, 0) + 1
        )

        self.hub_outgoing[source] = (
            self.hub_outgoing.get(source, 0) + 1
        )

        destination_hub = self.config.hubs[destination]

        if destination_hub.zone == ZoneTypes.RESTRICTED:
            self.next_hub_incoming[destination] = (
                self.next_hub_incoming.get(destination, 0)
                + 1
            )
        else:
            self.hub_incoming[destination] = (
                self.hub_incoming.get(destination, 0)
                + 1
            )
