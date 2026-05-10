"""Command-line interface for the habit tracker."""

from __future__ import annotations

from .domain import Periodicity
from .service import HabitService


class CLI:
    """Simple menu-driven command-line interface."""

    def __init__(self, service: HabitService) -> None:
        self.service = service

    def run(self) -> None:
        """Start the CLI loop."""
        print("Welcome to Habit Tracker")

        while True:
            print("\nMain menu")
            print("1) View habits")
            print("2) Create habit")
            print("3) Complete habit")
            print("4) Analyze habits")
            print("5) Edit habit")
            print("6) Archive habit")
            print("7) Delete habit")
            print("0) Exit")

            choice = input("Select an option: ").strip()

            try:
                if choice == "1":
                    self._show_habits()
                elif choice == "2":
                    self._create_habit()
                elif choice == "3":
                    self._complete_habit()
                elif choice == "4":
                    self._analyze_habits()
                elif choice == "5":
                    self._edit_habit()
                elif choice == "6":
                    self._archive_habit()
                elif choice == "7":
                    self._delete_habit()
                elif choice == "0":
                    print("Goodbye!")
                    return
                else:
                    print("Please choose a valid menu option.")

            except (ValueError, KeyError) as exc:
                print(f"Error: {exc}")

    def _show_habits(self) -> None:
        """Display all habits."""
        habits = self.service.get_all(include_archived=True)

        if not habits:
            print("No habits found yet.")
            return

        print("\nTracked habits")
        for habit in habits:
            status = "archived" if habit.archived else "active"
            print(
                f"[{habit.id}] {habit.name} | "
                f"{habit.periodicity.value} | "
                f"completions={len(habit.completions)} | "
                f"{status}"
            )

    def _list_habits_with_ids(self, include_archived: bool = False):
        """Display habits with their IDs and names."""
        habits = self.service.get_all(include_archived=include_archived)

        if not habits:
            print("No habits available.")
            return []

        print("\nAvailable habits:")
        for habit in habits:
            status = "archived" if habit.archived else "active"
            print(f"[{habit.id}] {habit.name} ({habit.periodicity.value}, {status})")

        return habits

    def _create_habit(self) -> None:
        """Create a new habit."""
        name = input("Habit name: ").strip()
        periodicity = self._ask_periodicity()
        notes = input("Notes (optional): ").strip()

        habit = self.service.create(name=name, periodicity=periodicity, notes=notes)
        print(f"Created habit [{habit.id}] {habit.name}.")

    def _complete_habit(self) -> None:
        """Record a completion."""
        habits = self._list_habits_with_ids()

        if not habits:
            return

        habit_id = input("\nEnter the ID of the habit you completed: ").strip()
        habit = self.service.complete(habit_id)

        print(f"Great! Completion recorded for '{habit.name}'.")

    def _edit_habit(self) -> None:
        """Edit a habit."""
        habits = self._list_habits_with_ids(include_archived=True)

        if not habits:
            return

        habit_id = input("\nEnter the ID of the habit to edit: ").strip()
        habit = self.service.get(habit_id)

        print(f"\nEditing '{habit.name}'")
        print("Leave a field blank to keep the current value.")

        name = input(f"New name [{habit.name}]: ").strip() or None
        periodicity_raw = input(
            f"New periodicity [{habit.periodicity.value}] (daily/weekly): "
        ).strip()
        periodicity = periodicity_raw or None
        notes = input(f"New notes [{habit.notes}]: ").strip() or None

        updated = self.service.edit(
            habit_id,
            name=name,
            periodicity=periodicity,
            notes=notes,
        )

        print(f"Habit '{updated.name}' updated.")

    def _archive_habit(self) -> None:
        """Archive a habit."""
        habits = self._list_habits_with_ids()

        if not habits:
            return

        habit_id = input("\nEnter the ID of the habit to archive: ").strip()
        self.service.archive(habit_id)

        print("Habit archived.")

    def _delete_habit(self) -> None:
        """Delete a habit permanently."""
        habits = self._list_habits_with_ids(include_archived=True)

        if not habits:
            return

        habit_id = input("\nEnter the ID of the habit to delete: ").strip()
        confirmation = input("Type DELETE to confirm permanent removal: ").strip()

        if confirmation != "DELETE":
            print("Deletion cancelled.")
            return

        self.service.delete(habit_id)
        print("Habit deleted.")

    def _analyze_habits(self) -> None:
        """Display analytics."""
        print("\nAnalytics")

        all_habits = self.service.get_all()
        print(f"Active habits: {len(all_habits)}")

        daily_habits = self.service.get_by_periodicity(Periodicity.DAILY)
        weekly_habits = self.service.get_by_periodicity(Periodicity.WEEKLY)

        daily_names = ", ".join(
            f"{habit.name} [{habit.id}]" for habit in daily_habits
        ) or "none"

        weekly_names = ", ".join(
            f"{habit.name} [{habit.id}]" for habit in weekly_habits
        ) or "none"

        print(f"Daily habits: {daily_names}")
        print(f"Weekly habits: {weekly_names}")

        best_name, best_streak = self.service.longest_streak_overall()
        if best_name:
            print(f"Longest streak overall: {best_name} ({best_streak})")
        else:
            print("Longest streak overall: none yet")

        habits = self._list_habits_with_ids()

        if not habits:
            return

        selected = input(
            "\nEnter a habit ID to view its longest streak, or press Enter to go back: "
        ).strip()

        if selected:
            streak = self.service.longest_streak_for(selected)
            habit = self.service.get(selected)
            print(f"Longest streak for '{habit.name}' [{habit.id}]: {streak}")

    @staticmethod
    def _ask_periodicity() -> Periodicity:
        """Ask the user for daily or weekly periodicity."""
        raw = input("Periodicity (daily/weekly): ").strip().lower()
        return Periodicity.from_value(raw)