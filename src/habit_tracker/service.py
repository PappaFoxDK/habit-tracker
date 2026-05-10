"""Application orchestration layer for the habit tracker."""

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional, Tuple

from . import analytics
from .domain import Habit, Periodicity
from .repository import HabitRepository


class HabitService:
    """Coordinates domain logic, persistence, and analytics."""

    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def create(self, name: str, periodicity: Any, notes: str = "") -> Habit:
        """Create and persist a new habit."""
        habit = Habit(
            id=self.repository.next_id(),
            name=name.strip(),
            periodicity=Periodicity.from_value(periodicity),
            created_at=datetime.utcnow(),
            notes=notes.strip(),
        )

        if not habit.name:
            raise ValueError("Habit name cannot be empty.")

        self.repository.upsert(habit)
        return habit

    def edit(
        self,
        habit_id: str,
        name: Optional[str] = None,
        periodicity: Optional[Any] = None,
        notes: Optional[str] = None,
    ) -> Habit:
        """Edit an existing habit."""
        habit = self.get(habit_id)

        if name is not None:
            habit.rename(name)

        if periodicity is not None:
            habit.set_periodicity(periodicity)

        if notes is not None:
            habit.notes = notes

        self.repository.upsert(habit)
        return habit

    def complete(self, habit_id: str, timestamp: Optional[datetime] = None) -> Habit:
        """Record a completion for a habit."""
        habit = self.get(habit_id)
        habit.mark_complete(timestamp)
        self.repository.upsert(habit)
        return habit

    def archive(self, habit_id: str) -> None:
        """Archive a habit."""
        self.repository.archive(habit_id)

    def delete(self, habit_id: str) -> None:
        """Delete a habit permanently."""
        self.repository.remove(habit_id)

    def get(self, habit_id: str) -> Habit:
        """Return one habit by ID."""
        for habit in self.repository.load():
            if habit.id == habit_id:
                return habit
        raise KeyError("Habit not found.")

    def get_all(self, include_archived: bool = False) -> List[Habit]:
        """Return all habits, optionally including archived ones."""
        habits = self.repository.load()
        return habits if include_archived else analytics.list_all(habits)

    def get_by_periodicity(self, periodicity: Any) -> List[Habit]:
        """Return all active habits with the selected periodicity."""
        return analytics.list_by_periodicity(
            self.repository.load(),
            Periodicity.from_value(periodicity),
        )

    def longest_streak_for(self, habit_id: str) -> int:
        """Return the longest streak for one habit."""
        return analytics.longest_streak_for(self.get(habit_id))

    def longest_streak_overall(self) -> Tuple[str, int]:
        """Return the best streak across all active habits."""
        return analytics.longest_streak_overall(self.repository.load())