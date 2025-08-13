from __future__ import annotations
import sys
from PyQt6.QtWidgets import QApplication
from gui import VotingWindow

def main() -> None:
    app = QApplication(sys.argv)
    w = VotingWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
