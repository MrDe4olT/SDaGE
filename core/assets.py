import os

import pygame


class AssetManager:
    def __init__(self) -> None:
        self.images = {}
        self.font_small = None
        self.font_big = None

    def load_image(self, path: str):
        return pygame.image.load(path).convert_alpha()

    def load_all(self) -> None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        images_dir = os.path.join(base_dir, "assets", "images")
        fonts_dir = os.path.join(base_dir, "assets", "fonts")

        self.images["office"] = self.load_image(os.path.join(images_dir, "Office.png"))
        self.images["monitor_work"] = self.load_image(os.path.join(images_dir, "Monitor_work.png"))
        self.images["monitor_generic"] = self.load_image(os.path.join(images_dir, "Monitor.png"))
        self.images["exit_btn"] = self.load_image(os.path.join(images_dir, "Exit_btn.png"))

        self.images["chosen_left"] = self.load_image(os.path.join(images_dir, "Chosen_monitor_left.png"))
        self.images["chosen_center"] = self.load_image(os.path.join(images_dir, "Chosen_monitor_center.png"))
        self.images["chosen_right"] = self.load_image(os.path.join(images_dir, "Chosen_monitor_right.png"))

        self.images["work_empty"] = self.load_image(os.path.join(images_dir, "Work_empty.png"))
        self.images["work_correct"] = self.load_image(os.path.join(images_dir, "Work_correct.png"))
        self.images["work_error"] = self.load_image(os.path.join(images_dir, "Work_error.png"))
        self.images["work_in_progress"] = self.load_image(os.path.join(images_dir, "Work_in_progress.png"))

        font_path = os.path.join(fonts_dir, "minecraft.ttf")
        self.font_small = pygame.font.Font(font_path, 24)
        self.font_big = pygame.font.Font(font_path, 40)