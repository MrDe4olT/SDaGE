import pygame

from core.gamestate import SceneBase


class RightCorridorScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the right corridor scene."""
        super().__init__(game)

        self.corridor_image = self.game.assets.images["corridor_right"]
        self.exit_button_image = self.game.assets.images["exit_btn"]

        door_button_width = self.exit_button_image.get_width()
        door_button_height = self.exit_button_image.get_height()
        self.exit_button_image = pygame.transform.smoothscale(self.exit_button_image, (door_button_width, door_button_height))
        self.exit_button_image = pygame.transform.rotate(self.exit_button_image, 90)
        self.exit_button_rect = self.exit_button_image.get_rect(midright=(1360, 540))

    def handle_event(self, event) -> None:
        """Handle scene events."""

    def update(self, dt: float) -> None:
        """Update session while player is looking at the right corridor."""
        session = self.game.session
        if session is None:
            return
        
        mouse_pos = pygame.mouse.get_pos()

        if self.exit_button_rect.collidepoint(mouse_pos):
            from ui.scenes.left_door_scene import LeftDoorScene
            self.game.change_scene(LeftDoorScene(self.game))
            return

        session.office.set_monitor("right_corridor")
        session.update(dt, False)

    def draw(self, screen) -> None:
        """Draw the right corridor and exit button."""
        screen.blit(self.corridor_image, (0, 0))
        screen.blit(self.exit_button_image, self.exit_button_rect.topleft)