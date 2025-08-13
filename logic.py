from __future__ import annotations
import csv
import os
import re
from typing import Dict

CSV_FILE = "voters.csv"

class VotingLogic:
    """Encapsulates vote storage and tallying.

    - Stores rows as: ID, Candidate
    - Validates: non-empty alphanumeric ID (plus _ and -), valid candidate
    """

    VALID_CANDIDATES = ("John", "Jane")
    ID_REGEX = re.compile(r"[A-Za-z0-9_-]{1,32}")

    def __init__(self, csv_path: str = CSV_FILE) -> None:
        self.csv_path = csv_path
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Candidate"])  # header

    def add_vote(self, voter_id: str, candidate: str) -> None:
        voter_id = (voter_id or "").strip()
        if not voter_id:
            raise ValueError("ID is required.")
        if not self.ID_REGEX.fullmatch(voter_id):
            raise ValueError("ID must be 1–32 chars: letters, numbers, _ or -.")
        if candidate not in self.VALID_CANDIDATES:
            raise ValueError("Please choose a candidate.")

        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([voter_id, candidate])

    def tally(self) -> Dict[str, int]:
        john = jane = 0
        with open(self.csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cand = (row.get("Candidate") or "").strip()
                if cand == "John":
                    john += 1
                elif cand == "Jane":
                    jane += 1
        return {"John": john, "Jane": jane, "Total": john + jane}
