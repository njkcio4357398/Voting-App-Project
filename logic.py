import csv
import os
from typing import Dict


class VoteManager:
    """
    Manages the vote data and tracks who has already voted.
    """
    def __init__(self, vote_file: str = "votes.csv", voter_file: str = "voters.csv"):
        self.vote_file = vote_file
        self.voter_file = voter_file
        self._votes = {"John": 0, "Jane": 0"}
        self._voters = set()
        self._load_votes()
        self._load_voters()

    def _load_votes(self) -> None:
        """Load existing votes from CSV file."""
        if os.path.exists(self.vote_file):
            try:
                with open(self.vote_file, mode="r", newline="") as file:
                    reader = csv.reader(file)
                    next(reader)  
                    for row in reader:
                        if row[0] in self._votes:
                            self._votes[row[0]] = int(row[1])
            except Exception as e:
                raise IOError(f"Failed to read vote data: {e}")

    def _save_votes(self) -> None:
        """Save votes to CSV file."""
        try:
            with open(self.vote_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Candidate", "Votes"])
                for candidate, count in self._votes.items():
                    writer.writerow([candidate, count])
        except Exception as e:
            raise IOError(f"Failed to save vote data: {e}")

    def add_vote(self, candidate: str, voter_name: str) -> None:
        """
        Adds a vote for the given candidate if the voter hasn't voted yet.

        Args:
            candidate (str): The candidate to vote for.
            voter_name (str): The name of the voter.

        Raises:
            ValueError: If the candidate is invalid or the voter already voted.
        """
        voter_name = voter_name.strip().lower()
        if candidate not in self._votes:
            raise ValueError("Invalid candidate")
        if voter_name in self._voters:
            raise ValueError("This voter has already voted")
        self._votes[candidate] += 1
        self._voters.add(voter_name)
        self._save_votes()
        self._save_voters()

    def get_results(self) -> Dict[str, int]:
        """Returns a copy of the current vote tally."""
        return self._votes.copy()
