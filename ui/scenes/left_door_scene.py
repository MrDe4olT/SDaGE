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

        door_button_width = self.exit_button_image.get_width()
        door_button_height = self.exit_button_image.get_height()
        self.exit_button_image = pygame.transform.smoothscale(self.exit_button_image, (door_button_width, door_button_height))
        self.exit_button_rect = self.exit_button_image.get_rect(midbottom = (960, 1080))

    def handle_event(self, event) -> None:
        """Handle scene events."""
        pass

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

        session.office.left_door_closed = (mouse_pressed and self.door_hold_rect.collidepoint(mouse_pos))

        session.office.set_monitor("left_door")
        session.update(dt, False)

    def draw(self, screen) -> None:
        """Draw the left door and exit button."""
        if self.game.session.office.left_door_closed:
            screen.blit(self.door_closed_image, (0, 0))
        else:
            screen.blit(self.door_opened_image, (0, 0))

        pygame.draw.rect(screen, (255, 0, 0), self.door_hold_rect, 2)

        screen.blit(self.exit_button_image, self.exit_button_rect.topleft)