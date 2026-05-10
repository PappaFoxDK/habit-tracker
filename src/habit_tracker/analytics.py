"""Functional analytics for habits."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Tuple

from .domain import Habit, Periodicity


def list_all(habits: Iterable[Habit]) -> List[Habit]:
    """Return all non-archived habits."""
    return [habit for habit in habits if not habit.archived]


def list_by_periodicity(habits: Iterable[Habit], periodicity: Periodicity) -> List[Habit]:
    """Return all non-archived habits with the given periodicity."""
    return [
        habit
        for habit in habits
        if not habit.archived and habit.periodicity == Periodicity.from_value(periodicity)
    ]


def longest_streak_for(habit: Habit) -> int:
    """Return the longest streak of consecutive fulfilled periods for a habit."""
    period_indexes = sorted(
        set(_period_index(timestamp, habit.periodicity) for timestamp in habit.completions)
    )

    if not period_indexes:
        return 0

    longest = 1
    current = 1

    for previous, current_value in zip(period_indexes, period_indexes[1:]):
        if current_value == previous + 1:
            current += 1
        else:
            if current > longest:
                longest = current
            current = 1

    return max(longest, current)


def longest_streak_overall(habits: Iterable[Habit]) -> Tuple[str, int]:
    """Return the habit name and streak length of the best streak overall."""
    active_habits = list(list_all(habits))

    if not active_habits:
        return "", 0

    scored = [(habit.name, longest_streak_for(habit)) for habit in active_habits]
    return max(scored, key=lambda item: item[1])


def streaks_by_habit(habits: Iterable[Habit]) -> Dict[str, int]:
    """Return a mapping of habit names to longest streak values."""
    return {habit.name: longest_streak_for(habit) for habit in list_all(habits)}


def _period_index(timestamp: datetime, periodicity: Periodicity) -> int:
    """Map a timestamp to a comparable period index."""
    ts = timestamp if timestamp.tzinfo is None else timestamp.astimezone().replace(tzinfo=None)
    ordinal = ts.date().toordinal()

    if periodicity == Periodicity.DAILY:
        return ordinal

    week_start = ts.date() - timedelta(days=ts.weekday())
    return week_start.toordinal() // 7