import pygame


class ProgressBar:
    def __init__(self, rect, bg_color, fill_color) -> None:
        self.rect = pygame.Rect(rect)
        self.bg_color = bg_color
        self.fill_color = fill_color

    def draw(self, screen, ratio: float) -> None:
        if ratio < 0.0:
            ratio = 0.0
        if ratio > 1.0:
            ratio = 1.0

        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=8)

        fill_rect = self.rect.copy()
        fill_rect.width = int(self.rect.width * ratio)
        pygame.draw.rect(screen, self.fill_color, fill_rect, border_radius=8)

        pygame.draw.rect(screen, (20, 20, 20), self.rect, 2, border_radius=8)