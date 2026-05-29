import pygame

from core.gamestate import SceneBase


class RelaxMonitorScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the relaxation monitor scene."""
        super().__init__(game)

        self.background_image = self.game.assets.images["monitor_generic"]
        self.exit_button_image = self.game.assets.images["exit_btn"]

        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()

        self.exit_button_rect = self.exit_button_image.get_rect()
        self.exit_button_rect.midbottom = (screen_width // 2, screen_height - 30)

    def handle_event(self, event) -> None:
        """Handle input events for the relaxation monitor."""
        pass

    def update(self, dt: float) -> None:
        """Update relaxation effects, session state, and scene transitions."""
        mouse_pos = pygame.mouse.get_pos()

        if self.exit_button_rect.collidepoint(mouse_pos):
            from ui.scenes.office_scene import OfficeScene

            self.game.change_scene(OfficeScene(self.game))
            return

        session = self.game.session
        session.office.set_monitor("right")
        session.update(dt, False)

        if not session.finished:
            return

        if session.result == "survived":
            from ui.scenes.win_scene import WinScene

            self.game.change_scene(WinScene(self.game))
        else:
            from ui.scenes.game_over_scene import GameOverScene

            self.game.change_scene(GameOverScene(self.game, session.result))

    def draw(self, screen) -> None:
        """Draw the relaxation monitor scene with a color overlay effect."""
        screen.blit(self.background_image, (0, 0))

        t = pygame.time.get_ticks()
        r = (t // 4) % 255
        g = (t // 6) % 255
        b = (t // 8) % 255

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((r, g, b, 100))
        screen.blit(overlay, (0, 0))

        screen.blit(self.exit_button_image, self.exit_button_rect.topleft)