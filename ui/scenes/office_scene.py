import pygame

from core.gamestate import SceneBase
from settings import DANGER_COLOR, TEXT_COLOR


class OfficeScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the main office overview scene."""
        super().__init__(game)

        self.game.session.office.set_monitor("center")

        self.office_image = self.game.assets.images["office"]
        self.chosen_left_image = self.game.assets.images["chosen_left"]
        self.chosen_center_image = self.game.assets.images["chosen_center"]
        self.chosen_right_image = self.game.assets.images["chosen_right"]

        self.center_monitor_rect = pygame.Rect(640, 243, 640, 400)

        self.left_monitor_polygon = [
            (184, 416),
            (620, 242),
            (620, 647),
            (184, 831),
        ]

        self.right_monitor_polygon = [
            (1300, 242),
            (1734, 416),
            (1734, 833),
            (1300, 646),
        ]

        self.hovered_monitor = None

    def handle_event(self, event) -> None:
        """Handle monitor clicks and switch to the selected monitor scene."""
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        mouse_pos = event.pos

        if self.point_in_polygon(mouse_pos, self.left_monitor_polygon):
            from ui.scenes.report_monitor_scene import ReportMonitorScene

            self.game.change_scene(ReportMonitorScene(self.game))
            return

        if self.center_monitor_rect.collidepoint(mouse_pos):
            from ui.scenes.work_monitor_scene import WorkMonitorScene

            self.game.change_scene(WorkMonitorScene(self.game))
            return

        if self.point_in_polygon(mouse_pos, self.right_monitor_polygon):
            from ui.scenes.relax_monitor_scene import RelaxMonitorScene

            self.game.change_scene(RelaxMonitorScene(self.game))

    def update(self, dt: float) -> None:
        """Update the office overview and react to session end states."""
        session = self.game.session

        if session is not None:
            session.office.set_monitor("center")
            session.update(dt, False)

            if session.finished:
                if session.result == "survived":
                    from ui.scenes.win_scene import WinScene

                    self.game.change_scene(WinScene(self.game))
                else:
                    from ui.scenes.game_over_scene import GameOverScene

                    self.game.change_scene(GameOverScene(self.game, session.result))
                return

        mouse_pos = pygame.mouse.get_pos()
        self.hovered_monitor = self.get_hovered_monitor(mouse_pos)

    def draw(self, screen) -> None:
        """Draw the office background, monitor highlight, overlay, and clock."""
        screen.blit(self.office_image, (0, 0))

        if self.hovered_monitor == "left":
            screen.blit(self.chosen_left_image, (0, 0))
        elif self.hovered_monitor == "center":
            screen.blit(self.chosen_center_image, (0, 0))
        elif self.hovered_monitor == "right":
            screen.blit(self.chosen_right_image, (0, 0))

        self.game.overlay.draw(screen, self.game.session)

        if self.game.session is None:
            return

        current_time = self.game.session.office.get_time_string()

        clock_bg = pygame.Rect(1600, 30, 220, 70)
        pygame.draw.rect(screen, (15, 15, 15), clock_bg, border_radius=12)
        pygame.draw.rect(screen, (90, 90, 90), clock_bg, 2, border_radius=12)

        clock_color = TEXT_COLOR
        if self.game.session.office.overtime_active:
            clock_color = DANGER_COLOR

        clock_text = self.game.big_font.render(current_time, True, clock_color)
        clock_text_rect = clock_text.get_rect(center=clock_bg.center)
        screen.blit(clock_text, clock_text_rect)

    def get_hovered_monitor(self, mouse_pos) -> str | None:
        """Return the monitor name currently hovered by the mouse."""
        if self.point_in_polygon(mouse_pos, self.left_monitor_polygon):
            return "left"

        if self.center_monitor_rect.collidepoint(mouse_pos):
            return "center"

        if self.point_in_polygon(mouse_pos, self.right_monitor_polygon):
            return "right"

        return None

    def point_in_polygon(self, point, polygon) -> bool:
        """Return True if a point lies inside the given polygon."""
        x, y = point
        inside = False
        count = len(polygon)

        for i in range(count):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % count]

            if (y1 > y) != (y2 > y):
                x_intersection = (x2 - x1) * (y - y1) / (y2 - y1) + x1
                if x < x_intersection:
                    inside = not inside

        return inside