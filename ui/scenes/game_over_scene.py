from core.gamestate import SceneBase
from settings import BG_COLOR, DANGER_COLOR, HEIGHT, TEXT_COLOR, WIDTH
from ui.widgets.button import Button


class GameOverScene(SceneBase):
    def __init__(self, game, reason: str) -> None:
        """Initialize the game over screen."""
        super().__init__(game)
        self.reason = reason
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
        """Update the game over scene state."""
        pass

    def draw(self, screen) -> None:
        """Draw the game over screen."""
        screen.fill(BG_COLOR)

        title = self.game.big_font.render("Game Over", True, DANGER_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(title, title_rect)

        if self.reason == "anxiety":
            reason_label = "You're too excited."
        elif self.reason == "killed_by_boss":
            reason_label = "Boss caught you."
        else:
            reason_label = str(self.reason)

        reason_text = self.game.font.render(reason_label, True, TEXT_COLOR)
        reason_rect = reason_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(reason_text, reason_rect)

        self.menu_button.draw(screen)