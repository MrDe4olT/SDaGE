import pygame

from core.gamestate import SceneBase


class LeftDoorScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the left door scene."""
        super().__init__(game)

        self.door_opened_image = pygame.transform.rotate(self.game.assets.images["door_opened"], 180)
        self.door_closed_image = self.game.assets.images["door_closed"]
        self.exit_button_image = self.game.assets.images["exit_btn"]

        self.door_hold_rect = pygame.Rect(125, 0, 1177, 1080)
        self.peek_rect = pygame.Rect(1300, 0, 507, 1080)

        door_button_width = self.exit_button_image.get_width()
        door_button_height = self.exit_button_image.get_height()
        self.exit_button_image = pygame.transform.smoothscale(
            self.exit_button_image,
            (door_button_width, door_button_height),
        )
        self.exit_button_rect = self.exit_button_image.get_rect(midbottom=(960, 1080))

    def handle_event(self, event) -> None:
        """Handle scene events."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.peek_rect.collidepoint(event.pos):
                from ui.scenes.left_corridor_scene import LeftCorridorScene
                self.game.change_scene(LeftCorridorScene(self.game))

    def update(self, dt: float) -> None:
        """Update left door state while the player is holding the mouse button."""
        session = self.game.session
        if session is None:
            return

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.exit_button_rect.collidepoint(mouse_pos):
            from ui.scenes.office_scene import OfficeScene
            self.game.change_scene(OfficeScene(self.game))
            return

        session.office.left_door_closed = (
            mouse_pressed and self.door_hold_rect.collidepoint(mouse_pos)
        )
        session.office.set_monitor("left_door")
        session.update(dt, False)

        if session.finished:
            if session.result == "survived":
                self.game.day = self.game.save_manager.next_day()
                self.game.day_config = self.game.difficulty_manager.get_day_config(self.game.day)

                if self.game.save_manager.is_game_completed():
                    from ui.scenes.win_scene import WinScene
                    self.game.change_scene(WinScene(self.game))
                else:
                    from ui.scenes.game_over_scene import GameOverScene
                    self.game.change_scene(GameOverScene(self.game, session.result))
            else:
                from ui.scenes.game_over_scene import GameOverScene
                self.game.change_scene(GameOverScene(self.game, session.result))

    def draw(self, screen) -> None:
        """Draw the left door, warning alert, and exit button."""
        office = self.game.session.office

        if office.left_door_closed:
            screen.blit(self.door_closed_image, (0, 0))
        else:
            screen.blit(self.door_opened_image, (0, 0))

        if office.should_show_left_door_alert():
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(220, 120, 120, 120))

        screen.blit(self.exit_button_image, self.exit_button_rect.topleft)