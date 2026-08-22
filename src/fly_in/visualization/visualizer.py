import pygame

from config import MapConfig
from simulation.state import SimulationState


class Visualizer:
    def __init__(self, config: MapConfig, state: SimulationState) -> None:
        self.width = 1000
        self.height = 700
        self.margin = 50
        pygame.init()

        self.config = config
        self.state = state
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 24)

        pygame.display.set_caption("Fly-in")

    def _get_position(
        self,
        x: int,
        y: int,
    ) -> tuple[int, int]:

        min_x = min(hub.x for hub in self.config.hubs.values())
        max_x = max(hub.x for hub in self.config.hubs.values())

        min_y = min(hub.y for hub in self.config.hubs.values())
        max_y = max(hub.y for hub in self.config.hubs.values())

        x_range = max(max_x - min_x, 1)
        y_range = max(max_y - min_y, 1)

        scale_x = (self.width - 100) / x_range
        scale_y = (self.height - 100) / y_range

        scale = min(scale_x, scale_y)

        graph_width = x_range * scale
        graph_height = y_range * scale

        offset_x = (self.width - graph_width) / 2
        offset_y = (self.height - graph_height) / 2

        screen_x = offset_x + (x - min_x) * scale

        screen_y = offset_y + (max_y - y) * scale

        return int(screen_x), int(screen_y)

    def _draw_connections(self) -> None:
        for connection in self.config.connections:
            hub_a = self.config.hubs[connection.hub_a]
            hub_b = self.config.hubs[connection.hub_b]

            position_a = self._get_position(
                hub_a.x,
                hub_a.y,
            )

            position_b = self._get_position(
                hub_b.x,
                hub_b.y,
            )

            pygame.draw.line(
                self.screen,
                (100, 100, 100),
                position_a,
                position_b,
                3,
            )

    def _draw_drones(self) -> None:
        for hub_name, hub_state in self.state.hubs.items():
            hub = self.config.hubs[hub_name]

            x, y = self._get_position(
                hub.x,
                hub.y,
            )

            drone_ids = sorted(hub_state.occupants)

            for i, drone_id in enumerate(drone_ids):
                row = i // 5
                column = i % 5

                drone_x = x - 20 + column * 10
                drone_y = y - 20 + row * 10

                pygame.draw.circle(
                    self.screen,
                    (0, 255, 255),
                    (drone_x, drone_y),
                    4,
                )

    def run(self) -> None:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((30, 30, 30))

            self._draw_connections()

            for hub in self.config.hubs.values():
                x, y = self._get_position(
                    hub.x,
                    hub.y,
                )

                try:
                    color = pygame.Color(hub.color)
                except ValueError:
                    color = pygame.Color("white")

                pygame.draw.circle(
                    self.screen,
                    color,
                    (x, y),
                    10,
                )

                mouse_x, mouse_y = pygame.mouse.get_pos()

                distance_x = mouse_x - x
                distance_y = mouse_y - y

                text = (
                    f"{hub.name} | "
                    f"zone: {hub.zone.value} | "
                    f"capacity: {hub.max_drones}"
                )

                if distance_x ** 2 + distance_y ** 2 <= 10 ** 2:
                    label = self.font.render(
                        text,
                        True,
                        (255, 255, 255),
                    )

                    self.screen.blit(
                        label,
                        (self.width - 450, 30),
                    )

            self._draw_drones()

            pygame.display.flip()

        pygame.quit()
