"""Data layer for storing tasks in JSON."""

import json
from pathlib import Path
from typing import Any


class TaskRepository:
    """Read and write tasks in a JSON file."""

    def __init__(self, filename: Path) -> None:
        self.filename = filename

    def load(self) -> list[dict[str, Any]]:
        """Return saved tasks or an empty list."""
        if not self.filename.exists():
            return []

        with self.filename.open("r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            raise ValueError("Invalid tasks file")

        return tasks

    def save(self, tasks: list[dict[str, Any]]) -> None:
        """Save tasks to a JSON file."""
        self.filename.parent.mkdir(parents=True, exist_ok=True)

        with self.filename.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
