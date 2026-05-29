import pygame

from core.gamestate import SceneBase
from settings import HEIGHT, TEXT_COLOR, WIDTH


class MenuScene(SceneBase):
    def handle_event(self, event) -> None:
        """Start a new day session after any key press."""
        if event.type != pygame.KEYDOWN:
            return

        from domain.day_session import DaySession
        from ui.scenes.office_scene import OfficeScene

        self.game.session = DaySession()
        self.game.change_scene(OfficeScene(self.game))

    def update(self, dt: float) -> None:
        """Update the menu scene state."""
        pass

    def draw(self, screen) -> None:
        """Draw the main menu screen."""
        screen.fill((10, 10, 10))

        title = self.game.big_font.render("SDaGE", True, TEXT_COLOR)
        hint = self.game.font.render("Press any key to start", True, TEXT_COLOR)

        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        screen.blit(title, title_rect)
        screen.blit(hint, hint_rect)