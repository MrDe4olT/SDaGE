from core.gamestate import SceneBase
from settings import BG_COLOR, GOOD_COLOR, HEIGHT, TEXT_COLOR, WIDTH
from ui.widgets.button import Button


class WinScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the victory screen."""
        super().__init__(game)
        self.menu_button = Button(
            (WIDTH // 2 - 120, HEIGHT // 2 + 80, 240, 60),
            "Back to menu",
            game.font,
        )

    def handle_event(self, event) -> None:
        """Handle clicks on the return-to-menu button."""
        if self.menu_button.is_clicked(event):
            from ui.scenes.menu_scene import MenuScene

            self.game.change_scene(MenuScene(self.game))

    def update(self, dt: float) -> None:
        """Update the win scene state."""
        pass

    def draw(self, screen) -> None:
        """Draw the victory screen."""
        screen.fill(BG_COLOR)

        title = self.game.big_font.render("You Survived", True, GOOD_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(title, title_rect)

        subtitle = self.game.font.render(
            "The work day is over. Time to go home.",
            True,
            TEXT_COLOR,
        )
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(subtitle, subtitle_rect)

        self.menu_button.draw(screen)