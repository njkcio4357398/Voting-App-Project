from __future__ import annotations
import csv
from pathlib import Path
from typing import Dict, Iterable, Set

BASE_DIR = Path(__file__).resolve().parent

class VoteManager:
    """
    Manages votes and tracks who has voted.
    Persists to:
      - votes.csv:  Candidate, Votes
      - voters.csv: Voter
    """

    def __init__(
        self,
        candidates: Iterable[str],
        vote_file: str | Path = "votes.csv",
        voter_file: str | Path = "voters.csv",
    ) -> None:
        self.vote_path = (BASE_DIR / vote_file) if not isinstance(vote_file, Path) else vote_file
        self.voter_path = (BASE_DIR / voter_file) if not isinstance(voter_file, Path) else voter_file

        self._candidates = [c for c in (candidates or []) if c]
        self._votes: Dict[str, int] = {c: 0 for c in self._candidates}
        self._voters: Set[str] = set()

        self._ensure_files()
        self._load_votes()
        self._load_voters()

    # ---------- file setup ----------
    def _ensure_files(self) -> None:
        if not self.vote_path.exists():
            with self.vote_path.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Candidate", "Votes"])
                for c in self._candidates:
                    w.writerow([c, 0])

        if not self.voter_path.exists():
            with self.voter_path.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Voter"])

    # ---------- load/save ----------
    def _load_votes(self) -> None:
        with self.vote_path.open("r", newline="", encoding="utf-8") as f:
            r = csv.reader(f)
            next(r, None)  # header
            for row in r:
                if len(row) >= 2 and row[0] in self._votes:
                    try:
                        self._votes[row[0]] = int(row[1])
                    except ValueError:
                        pass  # ignore bad rows

    def _save_votes(self) -> None:
        with self.vote_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Candidate", "Votes"])
            for c, n in self._votes.items():
                w.writerow([c, n])

    def _load_voters(self) -> None:
        with self.voter_path.open("r", newline="", encoding="utf-8") as f:
            r = csv.reader(f)
            next(r, None)  # header
            for row in r:
                if row and row[0].strip():
                    self._voters.add(row[0].strip().lower())

    def _save_voters(self) -> None:
        with self.voter_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Voter"])
            for v in sorted(self._voters):
                w.writerow([v])

    # ---------- public API ----------
    def add_vote(self, candidate: str, voter_name: str) -> None:
        voter_key = (voter_name or "").strip().lower()
        candidate = (candidate or "").strip()

        if not voter_key:
            raise ValueError("Please enter your name.")
        if candidate not in self._votes:
            raise ValueError("Please select a valid candidate.")
        if voter_key in self._voters:
            raise ValueError("This voter has already voted.")

        self._votes[candidate] += 1
        self._voters.add(voter_key)
        self._save_votes()
        self._save_voters()

    def get_results(self) -> Dict[str, int]:
        return dict(self._votes)
