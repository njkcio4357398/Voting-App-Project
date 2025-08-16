from __future__ import annotations
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox
from logic import VoteManager, BASE_DIR

class VotingApp(QWidget):
    """Main GUI window for the voting application (Qt Designer UI)."""

    def __init__(self) -> None:
        super().__init__()
        # Load the .ui built in Qt Designer
        uic.loadUi(str(BASE_DIR / "voting.ui"), self)

        # Read candidates from the ComboBox (skip the first blank)
        items = []
        for i in range(self.combo_box.count()):
            text = self.combo_box.itemText(i).strip()
            if text:  # ignore blank
                items.append(text)

        self.vote_manager = VoteManager(candidates=items)

        # Wire buttons
        self.vote_button.clicked.connect(self.cast_vote)
        self.results_button.clicked.connect(self.show_results)

    # ---- slots ----
    def cast_vote(self) -> None:
        voter = self.voter_input.text().strip()
        candidate = self.combo_box.currentText().strip()

        try:
            self.vote_manager.add_vote(candidate, voter)
        except Exception as e:
            self.status_label.setText(str(e))
            QMessageBox.warning(self, "Invalid Input", str(e))
            return

        self.status_label.setText("Vote recorded.")
        QMessageBox.information(self, "Success", f"{voter} voted for {candidate}.")
        self.voter_input.clear()
        self.combo_box.setCurrentIndex(0)

    def show_results(self) -> None:
        try:
            results = self.vote_manager.get_results()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        total = sum(results.values())
        lines = [f"{name}: {count} votes" for name, count in results.items()]
        lines.append(f"Total Votes: {total}")
        QMessageBox.information(self, "Voting Results", "\n".join(lines))
