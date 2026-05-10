from src.habit_tracker.cli import CLI
from src.habit_tracker.repository import HabitRepository
from src.habit_tracker.service import HabitService


def main() -> None:
    repository = HabitRepository("data/habits.json")
    service = HabitService(repository)
    cli = CLI(service)
    cli.run()


if __name__ == "__main__":
    main()