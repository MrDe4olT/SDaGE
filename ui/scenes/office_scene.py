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
        self.exit_button_image = self.game.assets.images["exit_btn"]
        self.screamer_image = self.game.assets.images["screamer"]

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

        door_button_width = self.exit_button_image.get_width() // 2
        door_button_height = self.exit_button_image.get_height() // 2

        self.exit_button_image = pygame.transform.smoothscale(self.exit_button_image, (door_button_width, door_button_height))

        self.left_door_button_image = pygame.transform.rotate(self.exit_button_image, 270)
        self.right_door_button_image = pygame.transform.rotate(self.exit_button_image, 90)

        self.left_door_button_rect = self.left_door_button_image.get_rect(midleft = (0, 540))
        self.right_door_button_rect = self.left_door_button_image.get_rect(midright = (1920, 540))

        self.hovered_monitor = None

    def handle_event(self, event) -> None:
        """Handle monitor clicks and switch to the selected monitor scene."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and (event.mod & pygame.KMOD_LSHIFT):
                self.game.session.finished = True
                self.game.session.result = "survived"
                return

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

    def update(self, dt: float) -> None:
        """Update the office overview and react to session end states."""
        session = self.game.session

        if session is not None:
            session.office.set_monitor("center")
            session.update(dt, False)

            if session.finished:
                if session.result == "survived":
                    self.game.day = self.game.save_manager.next_day()
                    self.game.day_config = self.game.difficulty_manager.get_day_config(self.game.day)
                    print("New day:", self.game.day)

                    if self.game.save_manager.is_game_completed():
                        print("Game completed")
                        from ui.scenes.win_scene import WinScene
                        self.game.change_scene(WinScene(self.game))
                    else:
                        from ui.scenes.game_over_scene import GameOverScene
                        self.game.change_scene(GameOverScene(self.game, session.result))
                else:
                    from ui.scenes.game_over_scene import GameOverScene
                    self.game.change_scene(GameOverScene(self.game, session.result))

            elif session.office.should_lose_from_boss():
                from ui.scenes.game_over_scene import GameOverScene
                self.game.change_scene(
                    GameOverScene(self.game, session.office.boss_attack_result or "killed_by_boss")
    )

        mouse_pos = pygame.mouse.get_pos()
        self.hovered_monitor = self.get_hovered_monitor(mouse_pos)

        if self.left_door_button_rect.collidepoint(mouse_pos):
            from ui.scenes.left_door_scene import LeftDoorScene

            self.game.change_scene(LeftDoorScene(self.game))
            return

        if self.right_door_button_rect.collidepoint(mouse_pos):
            from ui.scenes.right_door_scene import RightDoorScene

            self.game.change_scene(RightDoorScene(self.game))
            return

    def draw(self, screen) -> None:
        """Draw the office background, monitor highlight, overlay, and clock."""
        if self.game.session is not None and self.game.session.office.boss_jumpscare_active:
            screen.blit(self.screamer_image, (0, 0))
            return
        
        screen.blit(self.office_image, (0, 0))

        if self.hovered_monitor == "left":
            screen.blit(self.chosen_left_image, (0, 0))
        elif self.hovered_monitor == "center":
            screen.blit(self.chosen_center_image, (0, 0))
        elif self.hovered_monitor == "right":
            screen.blit(self.chosen_right_image, (0, 0))

        screen.blit(self.left_door_button_image, self.left_door_button_rect.topleft)
        screen.blit(self.right_door_button_image, self.right_door_button_rect.topleft)

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