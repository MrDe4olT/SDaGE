from settings import ANXIETY_MAX


class AnxietySystem:
    def __init__(
        self,
        max_value: float = ANXIETY_MAX,
        passive_gain_per_sec: float = 3.0,
        relief_per_sec: float = 12.0,
    ) -> None:
        """Initialize the anxiety system values and rates."""
        self.max_value = max_value
        self.value = 0.0
        self.passive_gain_per_sec = passive_gain_per_sec
        self.relief_per_sec = relief_per_sec

    def update(self, dt: float, is_relaxing: bool) -> None:
        """Update anxiety based on whether the player is relaxing."""
        if is_relaxing:
            self.value -= self.relief_per_sec * dt
        else:
            self.value += self.passive_gain_per_sec * dt

        if self.value < 0:
            self.value = 0.0

        if self.value > self.max_value:
            self.value = self.max_value

    def is_maxed(self) -> bool:
        """Return True when anxiety has reached its maximum."""
        return self.value >= self.max_value