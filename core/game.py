import sys

import pygame

from core.assets import AssetManager
from core.gamestate import GameStateManager
from settings import FPS, HEIGHT, TITLE, WIDTH
from ui.overlay import Overlay
from ui.scenes.game_over_scene import GameOverScene
from ui.scenes.menu_scene import MenuScene
from ui.scenes.win_scene import WinScene
from core.save_manager import SaveManager
from core.difficulty_manager import DifficultyManager


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.session = None
        self.assets = AssetManager()
        self.assets.load_all()
        self.font = self.assets.font_small
        self.big_font = self.assets.font_big
        self.state_manager = GameStateManager()
        self.state_manager.set_scene(MenuScene(self))
        self.overlay = Overlay()
        self.save_manager = SaveManager()
        self.difficulty_manager = DifficultyManager()
        self.day = 1
        self.day_config = None

    def change_scene(self, scene) -> None:
        self.state_manager.set_scene(scene)

    def quit(self) -> None:
        self.running = False

    def get_anxiety_ratio(self) -> float:
        if self.session is None:
            return 0.0
        anxiety_system = self.session.office.anxiety_system

        if anxiety_system.max_value <= 0:
            return 0.0
        ratio = anxiety_system.value / anxiety_system.max_value

        if ratio < 0.0:
            return 0.0
        if ratio > 1.0:
            return 1.0

        return ratio

    def draw_global_vignette(self) -> None:
        if self.session is None:
            return
        anxiety_system = self.session.office.anxiety_system
        anxiety = anxiety_system.value
        anxiety_max = anxiety_system.max_value

        if anxiety_max <= 0:
            return
        start_vignette = 25

        ratio = (anxiety - start_vignette) / (anxiety_max - start_vignette)
        if ratio < 0.0:
            ratio = 0.0
        if ratio > 1.0:
            ratio = 1.0

        width, height = self.screen.get_size()

        edge_alpha = int(240 * ratio)
        edge_thickness = int(110 * ratio)

        if edge_thickness > 0:
            top = pygame.Surface((width, edge_thickness))
            top.fill((0, 0, 0))
            top.set_alpha(edge_alpha)
            self.screen.blit(top, (0, 0))

            bottom = pygame.Surface((width, edge_thickness))
            bottom.fill((0, 0, 0))
            bottom.set_alpha(edge_alpha)
            self.screen.blit(bottom, (0, height - edge_thickness))

            left = pygame.Surface((edge_thickness, height))
            left.fill((0, 0, 0))
            left.set_alpha(edge_alpha)
            self.screen.blit(left, (0, 0))

            right = pygame.Surface((edge_thickness, height))
            right.fill((0, 0, 0))
            right.set_alpha(edge_alpha)
            self.screen.blit(right, (width - edge_thickness, 0))

        if anxiety >= 80:
            full_ratio = (anxiety - 80) / 20

            if full_ratio < 0.0:
                full_ratio = 0.0
            if full_ratio > 1.0:
                full_ratio = 1.0

            full_alpha = int(255 * full_ratio)

            full_overlay = pygame.Surface((width, height))
            full_overlay.fill((0, 0, 0))
            full_overlay.set_alpha(full_alpha)
            self.screen.blit(full_overlay, (0, 0))

    def should_draw_vignette(self) -> bool:
        scene = self.state_manager.current_scene

        if scene is None:
            return False

        if isinstance(scene, (MenuScene, GameOverScene, WinScene)):
            return False

        return True

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.running:
                break

            scene = self.state_manager.current_scene
            if scene is None:
                continue

            for event in events:
                scene.handle_event(event)

            scene.update(dt)
            scene.draw(self.screen)

            if self.should_draw_vignette():
                self.draw_global_vignette()

            pygame.display.flip()

        pygame.quit()
        sys.exit()