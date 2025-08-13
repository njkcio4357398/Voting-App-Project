from __future__ import annotations
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import QButtonGroup
from logic import VotingLogic

class VotingWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("voting.ui", self)

        # Logic layer
        self.logic = VotingLogic()

        # Group radio buttons (exclusive selection)
        self._group = QButtonGroup(self)
        self._group.addButton(self.radioJohn)
        self._group.addButton(self.radioJane)
        self._group.setExclusive(True)

        # Wire signals
        self.btnVote.clicked.connect(self.on_vote)
        self.btnResults.clicked.connect(self.on_results)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.on_about)

    def _selected_candidate(self) -> str | None:
        if self.radioJohn.isChecked():
            return "John"
        if self.radioJane.isChecked():
            return "Jane"
        return None

    def on_vote(self) -> None:
        voter_id = self.inputId.text().strip()
        candidate = self._selected_candidate()
        try:
            self.logic.add_vote(voter_id, candidate)
        except ValueError as e:
            self.lblStatus.setText(str(e))
            return

        # Success: clear status label, inputs, and selections
        self.lblStatus.setText("")
        self.inputId.clear()
        self._group.setExclusive(False)
        self.radioJohn.setChecked(False)
        self.radioJane.setChecked(False)
        self._group.setExclusive(True)

        QMessageBox.information(self, "Vote Recorded", "Your vote has been recorded.")

    def on_results(self) -> None:
        t = self.logic.tally()
        QMessageBox.information(
            self,
            "Current Results",
            f"John – {t['John']}\nJane – {t['Jane']}\nTotal – {t['Total']}"
        )

    def on_about(self) -> None:
        QMessageBox.about(
            self,
            "About",
            "Voting Application\nBuilt with PyQt6 + Qt Designer",
        )
