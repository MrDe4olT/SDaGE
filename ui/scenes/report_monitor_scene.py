import pygame


from core.gamestate import SceneBase


class ReportMonitorScene(SceneBase):
    def __init__(self, game) -> None:
        """Initialize the report writing monitor scene."""
        super().__init__(game)

        self.background_image = self.game.assets.images["monitor_generic"]
        self.exit_button_image = self.game.assets.images["exit_btn"]

        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()

        self.exit_button_rect = self.exit_button_image.get_rect()
        self.exit_button_rect.midbottom = (screen_width // 2, screen_height - 30)

        self.show_sent_until = 0

        self.text_area_rect = pygame.Rect(350, 220, 1220, 520)

    def handle_event(self, event) -> None:
        """Handle typing input for writing and sending reports."""
        office = self.game.session.office
        report = office.report_system

        if event.type != pygame.KEYDOWN:
            return

        if report.pending_reports <= 0:
            return

        if pygame.time.get_ticks() < self.show_sent_until:
            return

        if event.key == pygame.K_RETURN:
            if report.send_report():
                self.show_sent_until = pygame.time.get_ticks() + 3000
                office.finish_and_spawn_next_task()
            return

        if len(event.unicode) != 1:
            return

        if not event.unicode.isalpha():
            return

        if not report.is_writing:
            report.start_report()

        report.register_letter()

    def update(self, dt: float) -> None:
        """Update report writing state, office session, and scene transitions."""
        mouse_pos = pygame.mouse.get_pos()

        if self.exit_button_rect.collidepoint(mouse_pos):
            from ui.scenes.office_scene import OfficeScene

            self.game.change_scene(OfficeScene(self.game))
            return

        session = self.game.session
        office = session.office

        office.set_monitor("left")
        session.update(dt, False)

        if not session.finished:
            return

        if session.result == "survived":
            from ui.scenes.win_scene import WinScene

            self.game.change_scene(WinScene(self.game))
        else:
            from ui.scenes.game_over_scene import GameOverScene

            self.game.change_scene(GameOverScene(self.game, session.result))

    def draw_wrapped_text(
        self,
        screen,
        text: str,
        font,
        color,
        rect: pygame.Rect,
        line_spacing: int = 8,
    ) -> None:
        """Draw wrapped text inside the given rectangle."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if current_line == "":
                test_line = word
            else:
                test_line = current_line + " " + word

            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= rect.width:
                current_line = test_line
            else:
                if current_line != "":
                    lines.append(current_line)
                current_line = word

        if current_line != "":
            lines.append(current_line)

        y = rect.top
        line_height = font.get_height() + line_spacing

        for line in lines:
            if y + line_height > rect.bottom:
                break

            line_surface = font.render(line, True, color)
            screen.blit(line_surface, (rect.left, y))
            y += line_height

    def draw(self, screen) -> None:
        """Draw the report monitor UI and typed report contents."""
        office = self.game.session.office
        report = office.report_system

        screen.blit(self.background_image, (0, 0))
        screen.blit(self.exit_button_image, self.exit_button_rect.topleft)

        title_surface = self.game.assets.font_big.render("Bug Reporter", True, (1, 1, 1))
        title_rect = title_surface.get_rect(midtop=(screen.get_width() // 2, 40))
        screen.blit(title_surface, title_rect)

        if pygame.time.get_ticks() < self.show_sent_until:
            sent_text = self.game.assets.font_big.render("Report sent", True, (120, 255, 120))
            sent_rect = sent_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(sent_text, sent_rect)
            return

        if report.pending_reports <= 0:
            return

        paper_rect = self.text_area_rect
        pygame.draw.rect(screen, (245, 245, 245), paper_rect)
        pygame.draw.rect(screen, (180, 180, 180), paper_rect, 2)

        status_surface = self.game.assets.font_small.render(
            f"{report.current_letters}/{report.letters_needed}",
            True,
            (30, 30, 30),
        )
        screen.blit(status_surface, (paper_rect.left, paper_rect.top - 40))

        text_rect = pygame.Rect(
            paper_rect.left + 24,
            paper_rect.top + 24,
            paper_rect.width - 48,
            paper_rect.height - 48,
        )

        self.draw_wrapped_text(
            screen,
            report.typed_text,
            self.game.assets.font_small,
            (20, 20, 20),
            text_rect,
            8,
        )