from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QLineEdit
)
from logic import VoteManager


class VotingApp(QWidget):
    """
    Main GUI window for the voting application.
    Allows user to vote for a candidate and view results.
    """
    def __init__(self):
        """Initialize the voting app and setup the UI."""
        super().__init__()
        self.setWindowTitle("Voting App")
        self.vote_manager = VoteManager()
        self.setup_ui()

    def setup_ui(self) -> None:
        """Configure and display the GUI components."""
        layout = QVBoxLayout()

        self.voter_label = QLabel("Enter your name:")
        layout.addWidget(self.voter_label)

        self.voter_input = QLineEdit()
        layout.addWidget(self.voter_input)

        self.label = QLabel("Select a candidate to vote:")
        layout.addWidget(self.label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["", "Bianca", "Edward", "Felicia"])
        layout.addWidget(self.combo_box)

        self.vote_button = QPushButton("Vote")
        self.vote_button.clicked.connect(self.cast_vote)
        layout.addWidget(self.vote_button)

        self.results_button = QPushButton("Show Results")
        self.results_button.clicked.connect(self.show_results)
        layout.addWidget(self.results_button)

        self.setLayout(layout)

    def cast_vote(self) -> None:
        """Handles the voting process for a selected candidate and checks for duplicate voters."""
        voter = self.voter_input.text().strip()
        candidate = self.combo_box.currentText()

        if not voter:
            QMessageBox.warning(self, "Invalid Input", "Please enter your name.")
            return

        if candidate == "":
            QMessageBox.warning(self, "Invalid Input", "Please select a candidate.")
            return

        try:
            self.vote_manager.add_vote(candidate, voter)
            QMessageBox.information(self, "Success", f"{voter} voted for {candidate}.")
            self.voter_input.clear()
            self.combo_box.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_results(self) -> None:
        """Displays the current vote tally in a popup window."""
        try:
            results = self.vote_manager.get_results()
            message = "\n".join(f"{name}: {count} votes" for name, count in results.items())
            total = sum(results.values())
            message += f"\nTotal Votes: {total}"
            QMessageBox.information(self, "Voting Results", message)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
