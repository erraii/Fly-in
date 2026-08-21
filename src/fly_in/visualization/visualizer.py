import pygame

from config import MapConfig


class Visualizer:
    def __init__(self, config: MapConfig) -> None:
        self.width = 1000
        self.height = 700
        self.margin = 50
        pygame.init()

        self.config = config
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

    def run(self) -> None:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((30, 30, 30))

            self._draw_connections()

            for hub in self.config.hubs.values():
                # x = 100 + hub.x * 100
                # y = 350 - hub.y * 100
                x, y = self._get_position(
                    hub.x,
                    hub.y,
                )

                pygame.draw.circle(
                    self.screen,
                    (255, 255, 255),
                    (x, y),
                    10,
                )

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for hub in self.config.hubs.values():
                x, y = self._get_position(
                    hub.x,
                    hub.y,
                )

                pygame.draw.circle(
                    self.screen,
                    (255, 255, 255),
                    (x, y),
                    10,
                )

                distance_x = mouse_x - x
                distance_y = mouse_y - y

                if distance_x ** 2 + distance_y ** 2 <= 10 ** 2:
                    label = self.font.render(
                        hub.name,
                        True,
                        (255, 255, 255),
                    )

                    self.screen.blit(
                        label,
                        (x + 15, y - 10),
                    )

            pygame.display.flip()

        pygame.quit()
