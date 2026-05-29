from abc import ABC, abstractmethod


class SceneBase(ABC):
    def __init__(self, game) -> None:
        self.game = game
        self.use_global_vignette = True

    @abstractmethod
    def handle_event(self, event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        pass


class GameStateManager:
    def __init__(self) -> None:
        self.current_scene = None

    def set_scene(self, scene) -> None:
        self.current_scene = scene