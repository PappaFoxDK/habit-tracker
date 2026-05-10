from datetime import datetime

from habit_tracker.domain import Habit, Periodicity
from habit_tracker.repository import HabitRepository


def test_repository_roundtrip(tmp_path):
    path = tmp_path / "habits.json"
    repo = HabitRepository(str(path))

    habit = Habit(
        id="1",
        name="Meditate",
        periodicity=Periodicity.DAILY,
        created_at=datetime(2026, 2, 1, 8, 0, 0),
        notes="10 minutes",
    )

    repo.upsert(habit)
    loaded = repo.load()

    assert len(loaded) == 1
    assert loaded[0].name == "Meditate"
    assert loaded[0].notes == "10 minutes"
    assert loaded[0].periodicity == Periodicity.DAILY


def test_repository_archive_and_next_id(tmp_path):
    path = tmp_path / "habits.json"
    repo = HabitRepository(str(path))

    repo.save([
        Habit("1", "Read", Periodicity.DAILY, datetime(2026, 2, 1)),
        Habit("2", "Gym", Periodicity.WEEKLY, datetime(2026, 2, 1)),
    ])

    repo.archive("1")
    habits = repo.load()

    assert habits[0].archived is True
    assert repo.next_id() == "3"