import pygame

from core.gamestate import SceneBase


class LeftCorridorScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the left corridor scene."""
        super().__init__(game)

        self.corridor_image = self.game.assets.images["corridor_left"]
        self.exit_button_image = self.game.assets.images["exit_btn"]

        door_button_width = self.exit_button_image.get_width()
        door_button_height = self.exit_button_image.get_height()
        self.exit_button_image = pygame.transform.smoothscale(
            self.exit_button_image,
            (door_button_width, door_button_height),
        )
        self.exit_button_image = pygame.transform.rotate(self.exit_button_image, 270)
        self.exit_button_rect = self.exit_button_image.get_rect(midleft=(560, 540))

    def handle_event(self, event) -> None:
        """Handle scene events."""
        pass

    def update(self, dt: float) -> None:
        """Update session while player is looking at the left corridor."""
        session = self.game.session
        if session is None:
            return

        mouse_pos = pygame.mouse.get_pos()

        if self.exit_button_rect.collidepoint(mouse_pos):
            from ui.scenes.left_door_scene import LeftDoorScene
            self.game.change_scene(LeftDoorScene(self.game))
            return

        session.office.set_monitor("left_corridor")
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
        """Draw the left corridor and exit button."""
        screen.blit(self.corridor_image, (0, 0))
        screen.blit(self.exit_button_image, self.exit_button_rect.topleft)