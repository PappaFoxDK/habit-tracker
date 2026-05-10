from datetime import datetime

from habit_tracker.analytics import (
    longest_streak_for,
    longest_streak_overall,
    list_by_periodicity,
)
from habit_tracker.domain import Habit, Periodicity

def test_longest_streak_for_daily_habit():
    habit = Habit(
        id="1",
        name="Read",
        periodicity=Periodicity.DAILY,
        created_at=datetime(2026, 2, 1, 8, 0, 0),
        completions=[
            datetime(2026, 2, 1, 9, 0, 0),
            datetime(2026, 2, 2, 9, 0, 0),
            datetime(2026, 2, 3, 9, 0, 0),
            datetime(2026, 2, 5, 9, 0, 0),
        ],
    )

    assert longest_streak_for(habit) == 3


def test_list_by_periodicity_filters_active_habits_only():
    daily = Habit("1", "Read", Periodicity.DAILY, datetime(2026, 2, 1))
    weekly = Habit("2", "Gym", Periodicity.WEEKLY, datetime(2026, 2, 1), archived=True)

    result = list_by_periodicity([daily, weekly], Periodicity.DAILY)

    assert result == [daily]


def test_longest_streak_overall_returns_habit_name_and_score():
    daily = Habit(
        id="1",
        name="Read",
        periodicity=Periodicity.DAILY,
        created_at=datetime(2026, 2, 1),
        completions=[
            datetime(2026, 2, 1),
            datetime(2026, 2, 2),
        ],
    )

    weekly = Habit(
        id="2",
        name="Gym",
        periodicity=Periodicity.WEEKLY,
        created_at=datetime(2026, 2, 1),
        completions=[
            datetime(2026, 2, 2),
            datetime(2026, 2, 9),
            datetime(2026, 2, 16),
        ],
    )

    assert longest_streak_overall([daily, weekly]) == ("Gym", 3)