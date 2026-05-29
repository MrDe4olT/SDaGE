import pygame

from core.gamestate import SceneBase
from ui.widgets.progress_bar import ProgressBar


class WorkMonitorScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the work monitor scene and task grid."""
        super().__init__(game)

        self.holding_work = False

        self.background_image = self.game.assets.images["monitor_work"]
        self.exit_button_image = self.game.assets.images["exit_btn"]

        self.task_empty_image = self.game.assets.images["work_empty"]
        self.task_correct_image = self.game.assets.images["work_correct"]
        self.task_error_image = self.game.assets.images["work_error"]
        self.task_in_progress_image = self.game.assets.images["work_in_progress"]

        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()

        self.exit_button_rect = self.exit_button_image.get_rect()
        self.exit_button_rect.midbottom = (screen_width - 650, screen_height - 30)

        self.work_bar = ProgressBar(
            (screen_width - 650, screen_height - 900, 500, 50),
            (50, 50, 50),
            (80, 200, 120),
        )

        self.task_rects = []
        self.create_task_grid()

    def create_task_grid(self) -> None:
        """Create rectangles for all visible work task slots."""
        task_width = self.task_empty_image.get_width()
        task_height = self.task_empty_image.get_height()

        self.task_rects = []

        row1_y = 207
        row2_y = 553
        row3_y = 900

        start_x = 85
        gap = 85

        for i in range(5):
            x = start_x + i * (task_width + gap)
            self.task_rects.append(pygame.Rect(x, row1_y, task_width, task_height))

        for i in range(7):
            x = start_x + i * (task_width + gap)
            self.task_rects.append(pygame.Rect(x, row2_y, task_width, task_height))

        for i in range(3):
            x = start_x + i * (task_width + gap)
            self.task_rects.append(pygame.Rect(x, row3_y, task_width, task_height))

    def handle_event(self, event) -> None:
        """Handle starting and stopping work on a task slot."""
        office = self.game.session.office
        reports_pending = office.report_system.pending_reports > 0

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.holding_work = False

        if reports_pending:
            return

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        for index, rect in enumerate(self.task_rects):
            if not rect.collidepoint(event.pos):
                continue

            if index >= len(office.work_slots):
                return

            if office.work_slots[index] != "empty":
                return

            current_slot = office.current_task_slot_index
            task_in_progress = (
                office.task.progress > 0
                and not office.task.is_completed
                and not office.task.is_failed
            )

            if task_in_progress:
                if current_slot is None:
                    return
                if index != current_slot:
                    return

            if office.current_task_slot_index is None:
                office.current_task_slot_index = index

            if office.current_task_slot_index != index:
                return

            self.holding_work = True
            return

    def update(self, dt: float) -> None:
        """Update work progress, task slot states, and scene transitions."""
        mouse_pos = pygame.mouse.get_pos()

        if self.exit_button_rect.collidepoint(mouse_pos):
            from ui.scenes.office_scene import OfficeScene

            self.game.change_scene(OfficeScene(self.game))
            return

        session = self.game.session
        office = session.office
        office.set_monitor("center")

        reports_pending = office.report_system.pending_reports > 0
        active_slot_index = office.current_task_slot_index

        if reports_pending:
            self.holding_work = False
            session.update(dt, False)
        elif active_slot_index is None:
            session.update(dt, False)
        else:
            if active_slot_index >= len(office.work_slots):
                self.holding_work = False
                office.current_task_slot_index = None
                session.update(dt, False)
                return

            if office.work_slots[active_slot_index] != "empty":
                self.holding_work = False
                office.current_task_slot_index = None
                session.update(dt, False)
                return

            active_rect = self.task_rects[active_slot_index]

            if self.holding_work and not active_rect.collidepoint(mouse_pos):
                self.holding_work = False

            session.update(dt, self.holding_work)

            if office.task.is_completed:
                office.work_slots[active_slot_index] = "correct"
                self.holding_work = False
                office.current_task_slot_index = None
                office.finish_and_spawn_next_task()
            elif office.task.is_failed:
                office.work_slots[active_slot_index] = "error"
                self.holding_work = False
                office.current_task_slot_index = None

        if not session.finished:
            return

        if session.result == "survived":
            from ui.scenes.win_scene import WinScene

            self.game.change_scene(WinScene(self.game))
        else:
            from ui.scenes.game_over_scene import GameOverScene

            self.game.change_scene(GameOverScene(self.game, session.result))

    def draw(self, screen) -> None:
        """Draw the work monitor, task slots, and progress bar."""
        office = self.game.session.office
        reports_pending = office.report_system.pending_reports > 0
        active_slot_index = office.current_task_slot_index

        screen.blit(self.background_image, (0, 0))
        screen.blit(self.exit_button_image, self.exit_button_rect.topleft)

        for index, rect in enumerate(self.task_rects):
            slot_state = "empty"

            if index < len(office.work_slots):
                slot_state = office.work_slots[index]

            if slot_state == "correct":
                image = self.task_correct_image
            elif slot_state == "error":
                image = self.task_error_image
            elif (
                index == active_slot_index
                and not office.task.is_completed
                and not office.task.is_failed
            ):
                image = self.task_in_progress_image
            else:
                image = self.task_empty_image

            screen.blit(image, rect.topleft)

        ratio = 0.0
        if not reports_pending and office.task.hold_time > 0:
            ratio = office.task.progress / office.task.hold_time
            if ratio > 1.0:
                ratio = 1.0

        self.work_bar.draw(screen, ratio)