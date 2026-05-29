import random

from settings import TASK_FAIL_CHANCE


class WorkTask:
    def __init__(self, hold_time: float = 4.0, fail_chance: float = TASK_FAIL_CHANCE) -> None:
        """Initialize a work task with progress and failure settings."""
        self.hold_time = hold_time
        self.fail_chance = fail_chance
        self.progress = 0.0
        self.is_completed = False
        self.is_failed = False

    def update(self, dt: float, is_holding_work_button: bool) -> None:
        """Advance task progress while the work action is being held."""
        if self.is_completed or self.is_failed:
            return

        if not is_holding_work_button:
            return

        self.progress += dt

        if self.progress >= self.hold_time:
            if random.random() < self.fail_chance:
                self.is_failed = True
            else:
                self.is_completed = True

    def reset(self, hold_time: float | None = None) -> None:
        """Reset task state for a new work item."""
        if hold_time is not None:
            self.hold_time = hold_time

        self.progress = 0.0
        self.is_completed = False
        self.is_failed = False