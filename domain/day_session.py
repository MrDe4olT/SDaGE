from domain.office_state import OfficeState


class DaySession:
    def __init__(self) -> None:
        """Initialize a single workday session."""
        self.office = OfficeState()
        self.finished = False
        self.result = None

    def update(self, dt: float, is_holding_work_button: bool) -> None:
        """Update the active day session and check end conditions."""
        if self.finished:
            return

        self.office.update(dt, is_holding_work_button)

        if self.office.is_game_over():
            self.finished = True
            self.result = "anxiety"
            return

        if self.office.is_day_finished() and self.office.is_win_condition_met():
            self.finished = True
            self.result = "survived"
            return

        if self.office.should_lose_from_time():
            self.finished = True
            self.result = "Timeout"