from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QLineEdit
)
from logic import VoteManager

class VotingApp(QWidget):
    """
    Main GUI window for the voting application.
    Allows user to vote for a candidate and view results.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Voting App")
        self.vote_manager = VoteManager()  # defaults to John/Jane
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter your name:"))
        self.voter_input = QLineEdit()
        layout.addWidget(self.voter_input)

        layout.addWidget(QLabel("Select a candidate to vote:"))
        self.combo_box = QComboBox()
        self.combo_box.addItems(["", "John", "Jane"])  # <-- John & Jane here
        layout.addWidget(self.combo_box)

        self.vote_button = QPushButton("Vote")
        self.vote_button.clicked.connect(self.cast_vote)
        layout.addWidget(self.vote_button)

        self.results_button = QPushButton("Show Results")
        self.results_button.clicked.connect(self.show_results)
        layout.addWidget(self.results_button)

        self.setLayout(layout)

    def cast_vote(self) -> None:
        voter = self.voter_input.text().strip()
        candidate = self.combo_box.currentText().strip()

        if not voter:
            QMessageBox.warning(self, "Invalid Input", "Please enter your name.")
            return
        if candidate == "":
            QMessageBox.warning(self, "Invalid Input", "Please select a candidate.")
            return

        try:
            self.vote_manager.add_vote(candidate, voter)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

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
        message = "\n".join(f"{name}: {count} votes" for name, count in results.items())
        message += f"\nTotal Votes: {total}"
        QMessageBox.information(self, "Voting Results", message)
