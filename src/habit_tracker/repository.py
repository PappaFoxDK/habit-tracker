"""Persistence layer for habits using JSON storage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from .domain import Habit


class HabitRepository:
    """Repository that stores habits in a JSON file."""

    def __init__(self, path: str = "habit_fixture.json") -> None:
        self.path = Path(path)

    def load(self) -> List[Habit]:
        """Load all habits from the repository."""
        if not self.path.exists():
            self._write_payload({
                "version": 1,
                "exported_at": None,
                "habits": [],
            })
            return []

        with self.path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        return [Habit.from_dict(item) for item in payload.get("habits", [])]

    def save(self, habits: List[Habit]) -> None:
        """Save all habits to the repository."""
        self._write_payload({
            "version": 1,
            "exported_at": None,
            "habits": [habit.to_dict() for habit in habits],
        })

    def upsert(self, habit: Habit) -> None:
        """Insert a new habit or update an existing one."""
        habits = self.load()
        updated = False

        for index, current in enumerate(habits):
            if current.id == habit.id:
                habits[index] = habit
                updated = True
                break

        if not updated:
            habits.append(habit)

        self.save(habits)

    def archive(self, habit_id: str) -> None:
        """Archive a habit by ID."""
        habits = self.load()
        target = self._find(habits, habit_id)

        if target is None:
            raise KeyError("Habit not found.")

        target.archive()
        self.save(habits)

    def remove(self, habit_id: str) -> None:
        """Delete a habit permanently by ID."""
        habits = self.load()
        filtered = [habit for habit in habits if habit.id != habit_id]

        if len(filtered) == len(habits):
            raise KeyError("Habit not found.")

        self.save(filtered)

    def next_id(self) -> str:
        """Return the next available numeric ID as a string."""
        habits = self.load()
        numeric_ids = []

        for habit in habits:
            try:
                numeric_ids.append(int(habit.id))
            except ValueError:
                continue

        return str(max(numeric_ids, default=0) + 1)

    @staticmethod
    def _find(habits: List[Habit], habit_id: str) -> Optional[Habit]:
        """Find a habit by ID."""
        for habit in habits:
            if habit.id == habit_id:
                return habit
        return None

    def _write_payload(self, payload: dict) -> None:
        """Write the JSON payload to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")