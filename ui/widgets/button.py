import pygame

from settings import PANEL_ACTIVE_COLOR, PANEL_COLOR, TEXT_COLOR


class Button:
    def __init__(self, rect, text: str, font) -> None:
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

    def draw(self, screen, active: bool = False) -> None:
        color = PANEL_ACTIVE_COLOR if active else PANEL_COLOR

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (90, 90, 90), self.rect, 2, border_radius=10)

        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )