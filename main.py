from __future__ import annotations
import sys
from PyQt6.QtWidgets import QApplication
from gui import VotingApp

def main() -> None:
    """Entry point for the voting application."""
    app = QApplication(sys.argv)
    window = VotingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
