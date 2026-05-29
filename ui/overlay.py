import pygame


class Overlay:
    def __init__(self) -> None:
        """Initialize the debug overlay."""
        self.enabled = True
        self.font = pygame.font.SysFont("arial", 24)

    def toggle(self) -> None:
        """Toggle overlay visibility on and off."""
        self.enabled = not self.enabled

    def draw(self, screen, session) -> None:
        """Draw debug information for the current session."""
        if not self.enabled or session is None:
            return

        office = session.office
        report = office.report_system

        lines = [
            # f"time: {office.get_time_string()}",
            # f"monitor: {office.selected_monitor}",
            # f"anxiety: {int(office.anxiety_system.value)} / {int(office.anxiety_system.max_value)}",
            # f"task progress: {office.task.progress:.1f} / {office.task.hold_time}",
            # f"task completed: {office.task.is_completed}",
            # f"task failed: {office.task.is_failed}",
            # f"pending reports: {report.pending_reports}",
            # f"report letters: {report.current_letters} / {report.letters_needed}",
            # f"report writing: {report.is_writing}",
            # f"active task slot: {office.current_task_slot_index}",
            # f"finished: {session.finished}",
            # f"result: {session.result}",
        ]

        x = 20
        y = 20

        for line in lines:
            text = self.font.render(line, True, (1, 1, 1))
            screen.blit(text, (x, y))
            y += 28