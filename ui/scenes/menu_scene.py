import pygame

from core.gamestate import SceneBase
from settings import HEIGHT, TEXT_COLOR, WIDTH, BG_COLOR


class MenuScene(SceneBase):
    def __init__(self, game):
        self.game = game
        self.selected = -1

        self.buttons = ["New Game", "Continue", "Settings", "Quit"]
        self.rects = []

        button_weight = 320
        button_height = 60
        gap = 20

        for i in range(len(self.buttons)):
            rect = pygame.Rect(WIDTH // 12 , HEIGHT // 1.8 + i * (button_height + gap), button_weight, button_height)
            self.rects.append(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.selected = -1
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.selected = i
                    break

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    name = self.buttons[i]

                    if name == "New Game":
                        from domain.day_session import DaySession
                        from ui.scenes.office_scene import OfficeScene

                        self.game.save_manager.set_day(1)
                        self.game.day = self.game.save_manager.get_day()
                        self.game.day_config = self.game.difficulty_manager.get_day_config(self.game.day)
                        self.game.session = DaySession(self.game.day, self.game.day_config)
                        self.game.change_scene(OfficeScene(self.game))
                        self.game.save_manager.set_has_save(True)
                        self.game.save_manager.set_game_completed(False)

                    elif name == "Continue":
                        if not self.game.save_manager.has_save():
                            return
                        
                        if self.game.save_manager.is_game_completed():
                            return
                        
                        from domain.day_session import DaySession
                        from ui.scenes.office_scene import OfficeScene

                        self.game.day = self.game.save_manager.get_day()
                        self.game.day_config = self.game.difficulty_manager.get_day_config(self.game.day)
                        self.game.session = DaySession(self.game.day, self.game.day_config)
                        self.game.change_scene(OfficeScene(self.game))

                    elif name == "Settings":
                       pass

                    elif name == "Quit":
                        self.game.quit()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BG_COLOR)

        title = self.game.big_font.render("SDaGE", True, TEXT_COLOR)
        screen.blit(title, title.get_rect(center=(WIDTH // 7 - 30, HEIGHT // 3)))

        have_save_to_continue = self.game.save_manager.has_save()
        game_completed = self.game.save_manager.is_game_completed()

        for i, rect in enumerate(self.rects):
            if i == self.selected:
                bg = (210, 210, 210)
                border = (255, 255, 255)
                color = (15, 15, 15)
            else:
                bg = (30, 30, 30)
                border = (90, 90, 90)
                color = TEXT_COLOR

            if self.buttons[i] == "Continue" and (not have_save_to_continue or game_completed):
                bg = (45, 45, 45)
                border = (70, 70, 70)
                color = (120, 120, 120)

            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, border, rect, 2, border_radius=10)

            text = self.game.font.render(self.buttons[i], True, color)
            screen.blit(text, text.get_rect(center=rect.center))

