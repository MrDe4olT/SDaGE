import random


class ReportSystem:
    def __init__(self) -> None:
        """Initialize the report writing system."""
        self.pending_reports = 0
        self.current_letters = 0
        self.letters_needed = 0
        self.is_writing = False
        self.typed_text = ""

    def add_report(self) -> None:
        """Add one pending report to the queue."""
        self.pending_reports += 1

        if self.pending_reports > 0 and self.letters_needed == 0:
            self.current_letters = 0
            self.letters_needed = random.randint(25, 70)
            self.typed_text = ""

    def start_report(self) -> bool:
        """Start writing a report if one is pending and assign a random letter goal."""
        if self.pending_reports <= 0:
            return False

        if self.is_writing:
            return True

        self.is_writing = True

        if self.letters_needed == 0:
            self.current_letters = 0
            self.letters_needed = random.randint(25, 70)

        return True

    def register_letter(self) -> bool:
        """Register one typed letter for the current report."""
        if not self.is_writing:
            return False

        if self.current_letters >= self.letters_needed:
            return False

        self.current_letters += 1
        self.typed_text += "Text "
        return True

    def send_report(self) -> bool:
        """Send the current report if enough letters were typed."""
        if not self.is_writing:
            return False

        if self.current_letters < self.letters_needed:
            return False

        self.pending_reports -= 1
        self.current_letters = 0
        self.letters_needed = 0
        self.is_writing = False
        self.typed_text = ""
        return True

    def cancel_current_report(self) -> None:
        """Cancel the current report writing state."""
        self.current_letters = 0
        self.letters_needed = 0
        self.is_writing = False
        self.typed_text = ""