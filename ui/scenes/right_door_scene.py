import pygame

from core.gamestate import SceneBase


class RightDoorScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the right door scene."""
        super().__init__(game)

        self.door_opened_image = self.game.assets.images["door_opened"]
        self.door_closed_image = self.game.assets.images["door_closed"]
        self.exit_button_image = self.game.assets.images["exit_btn"]

        self.door_hold_rect = pygame.Rect(617, 0, 1177, 1080)
        self.peek_rect = pygame.Rect(115, 0, 505, 1080)

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
                from ui.scenes.right_corridor_scene import RightCorridorScene
                self.game.change_scene(RightCorridorScene(self.game))

    def update(self, dt: float) -> None:
        """Update right door state while the player is holding the mouse button."""
        session = self.game.session
        if session is None:
            return

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.exit_button_rect.collidepoint(mouse_pos):
            from ui.scenes.office_scene import OfficeScene
            self.game.change_scene(OfficeScene(self.game))
            return

        session.office.right_door_closed = (
            mouse_pressed and self.door_hold_rect.collidepoint(mouse_pos)
        )
        session.office.set_monitor("right_door")
        session.update(dt, False)

    def draw(self, screen) -> None:
        """Draw the right door and exit button."""
        if self.game.session.office.right_door_closed:
            screen.blit(self.door_closed_image, (0, 0))
        else:
            screen.blit(self.door_opened_image, (0, 0))

        # pygame.draw.rect(screen, (255, 0, 0), self.door_hold_rect, 2)
        # pygame.draw.rect(screen, (0, 255, 0), self.peek_rect, 2)

        screen.blit(self.exit_button_image, self.exit_button_rect.topleft)