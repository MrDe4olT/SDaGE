import random

from domain.anxiety import AnxietySystem
from domain.report import ReportSystem
from domain.work import WorkTask
from settings import (
    ANXIETY_MAX,
    DAY_END_HOUR,
    DAY_SPEED_MINUTES_PER_SEC,
    DAY_START_HOUR,
    WORK_SLOT_COUNT,
)


class OfficeState:
    def __init__(self, day_config) -> None:
        """Initialize the full office gameplay state for one day."""
        self.selected_monitor = "center"
        self.day_config = day_config

        self.anxiety_system = AnxietySystem(
            ANXIETY_MAX,
            self.day_config["ANXIETY_PASSIVE_GAIN_PER_SEC"],
            self.day_config["ANXIETY_RELIEF_PER_SEC"]
        )

        self.task = WorkTask(
            hold_time=self.generate_random_task_hold_time(),
            fail_chance=self.day_config["TASK_FAIL_CHANCE"],
        )

        self.report_system = ReportSystem()
        self.day_time_minutes = DAY_START_HOUR * 60
        self.day_end_minutes = DAY_END_HOUR * 60

        self.work_slots = ["empty"] * WORK_SLOT_COUNT
        self.current_task_slot_index = None

        self.overtime_active = False
        self.overtime_end_minutes = (DAY_END_HOUR + 1) * 60

        self.left_door_closed = False
        self.right_door_closed = False

        self.boss_side = None
        self.boss_stage = None
        self.boss_visible = False
        self.boss_spawn_timer = self.generate_random_boss_spawn_time()
        self.boss_stage_timer = 0.0

    def set_monitor(self, monitor: str) -> None:
        """Set the currently active monitor."""
        self.selected_monitor = monitor

    def update(self, dt: float, is_holding_work_button: bool) -> None:
        """Update office time, anxiety, work task, and simple boss stages."""
        self.day_time_minutes += dt * DAY_SPEED_MINUTES_PER_SEC

        is_relaxing = self.selected_monitor == "right"
        self.anxiety_system.update(dt, is_relaxing)

        self.task.update(dt, is_holding_work_button)

        if self.task.is_failed and self.report_system.pending_reports <= 0:
            self.report_system.add_report()

        if not self.boss_visible:
            self.boss_spawn_timer -= dt
            if self.boss_spawn_timer <= 0:
                self.boss_visible = True
                self.boss_side = random.choice(["left", "right"])
                self.boss_stage = "far"
                self.boss_stage_timer = self.generate_random_boss_mid_time()
        else:
            if self.boss_stage == "far":
                self.boss_stage_timer -= dt
                if self.boss_stage_timer <= 0:
                    self.boss_stage = "mid"

        if not self.overtime_active and self.day_time_minutes >= self.day_end_minutes:
            if not self.is_win_condition_met():
                self.overtime_active = True

        max_time = self.overtime_end_minutes if self.overtime_active else self.day_end_minutes
        if self.day_time_minutes > max_time:
            self.day_time_minutes = max_time

    def hide_boss(self) -> None:
        """Hide boss and start a new random spawn timer."""
        self.boss_visible = False
        self.boss_side = None
        self.boss_stage = None
        self.boss_spawn_timer = self.generate_random_boss_spawn_time()
        self.boss_stage_timer = 0.0

    def generate_random_task_hold_time(self) -> float:
        """Return a random duration for the next work task."""
        return random.uniform(3, 12)

    def generate_random_boss_spawn_time(self) -> float:
        """Return a random duration before boss appears again."""
        return random.uniform(8, 16)

    def generate_random_boss_mid_time(self) -> float:
        """Return a random duration before boss moves from far to mid."""
        return random.uniform(4, 7)

    def get_time_string(self) -> str:
        """Return the current in-game time as HH:MM."""
        total_minutes = int(self.day_time_minutes)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def finish_and_spawn_next_task(self) -> None:
        """Reset the current task so a new task can be started."""
        self.task = WorkTask(
            hold_time=self.generate_random_task_hold_time(),
            fail_chance=self.day_config["TASK_FAIL_CHANCE"],
        )
        self.current_task_slot_index = None

    def are_all_task_slots_closed(self) -> bool:
        """Return True when every task slot is either correct or error."""
        for slot in self.work_slots:
            if slot not in ("correct", "error"):
                return False
        return True

    def has_unresolved_reports(self) -> bool:
        """Return True when there are reports still waiting to be sent."""
        return self.report_system.pending_reports > 0 or self.report_system.is_writing

    def is_win_condition_met(self) -> bool:
        """Return True when all task slots are closed and no report is pending."""
        return self.are_all_task_slots_closed() and not self.has_unresolved_reports()

    def is_game_over(self) -> bool:
        """Return True when the anxiety game-over condition is reached."""
        return self.anxiety_system.is_maxed()

    def is_day_finished(self) -> bool:
        """Return True when normal day time has reached its end."""
        return self.day_time_minutes >= self.day_end_minutes

    def is_overtime_finished(self) -> bool:
        """Return True when overtime has fully expired."""
        return self.overtime_active and self.day_time_minutes >= self.overtime_end_minutes

    def should_lose_from_time(self) -> bool:
        """Return True when time has expired and tasks or reports are still unresolved."""
        if not self.is_overtime_finished():
            return False

        if not self.are_all_task_slots_closed():
            return True

        if self.has_unresolved_reports():
            return True

        return False