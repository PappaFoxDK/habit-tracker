# Habit Tracker

A command-line habit tracking application written in Python.
The app lets you create, complete, and analyze daily and weekly habits.
All data is stored locally in a JSON file and persists between sessions.

---

## Features

- Create habits with daily or weekly frequency
- Mark habits as complete
- Edit habit name, periodicity, or notes
- Archive habits you no longer want to track
- Delete habits permanently
- View all tracked habits and their completion counts
- See the longest streak for any individual habit
- See the overall longest streak across all habits
- Filter habits by daily or weekly periodicity
- Includes 5 predefined sample habits with 4 weeks of example data

---

## Project Structure

```
HabitTracker/
├── app.py                        # Entry point
├── conftest.py                   # Pytest path configuration
├── requirements.txt              # Dependencies
├── data/
│   └── habits.json               # Your habit data (created on first run)
├── src/
│   └── habit_tracker/
│       ├── domain.py             # Habit model and Periodicity enum
│       ├── repository.py         # JSON persistence layer
│       ├── service.py            # Application logic
│       ├── analytics.py          # Functional analytics (streaks, filtering)
│       └── cli.py                # Command-line interface
└── tests/
    ├── fixtures/
    │   └── habit_fixture.json    # Sample data used by tests
    ├── test_analytics.py         # Tests for analytics functions
    └── test_repository.py        # Tests for the repository layer
```

---

## Requirements

- Python 3.7 or higher
- pytest (for running tests)

---

## Installation

**1. Clone or unzip the project**

```bash
git clone https://github.com/your-username/habit-tracker.git
cd habit-tracker
```

Or if you downloaded the ZIP file, extract it and navigate into the folder:

```bash
cd HabitTracker
```

**2. (Optional) Create a virtual environment**

This keeps the project dependencies separate from your system Python.

```bash
python -m venv venv
```

Activate it:

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python app.py
```

You will see the main menu:

```
Welcome to Habit Tracker

Main menu
1) View habits
2) Create habit
3) Complete habit
4) Analyze habits
5) Edit habit
6) Archive habit
7) Delete habit
0) Exit
```

Type the number for the action you want and press Enter.

Your habits are saved to `data/habits.json` automatically after every change.

---

## How to Use

### Creating a Habit

1. Select **2) Create habit** from the main menu
2. Enter a name for the habit (e.g. `Read books`)
3. Enter the periodicity: type `daily` or `weekly`
4. Optionally enter a short note, or press Enter to skip

### Completing a Habit

1. Select **3) Complete habit**
2. The app shows a list of your active habits with their IDs
3. Enter the ID of the habit you completed
4. The current timestamp is recorded as a completion

### Viewing Your Habits

Select **1) View habits** to see all habits, including archived ones.
Each habit shows its ID, name, periodicity, total completion count, and status.

### Editing a Habit

1. Select **5) Edit habit**
2. Enter the ID of the habit you want to change
3. The app shows the current values — press Enter to keep any field as it is
4. You can change the name, periodicity, or notes

### Archiving a Habit

Archiving hides a habit from the active list without deleting its data.
This is useful when you want to stop tracking something but keep the history.

1. Select **6) Archive habit**
2. Enter the ID of the habit to archive

Archived habits still appear in the full habit list (option 1) and can still be edited.

### Deleting a Habit

Deletion is permanent and removes all history for that habit.

1. Select **7) Delete habit**
2. Enter the ID of the habit
3. Type `DELETE` (in uppercase) to confirm

### Analyzing Habits

Select **4) Analyze habits** to see:

- Total number of active habits
- Which habits are daily and which are weekly
- The habit with the overall longest streak
- An option to look up the longest streak for one specific habit

A **streak** is the number of consecutive periods (days or weeks) where you completed the habit at least once.

---

## Running the Tests

Make sure you are in the project root folder, then run:

```bash
python -m pytest tests/
```

To see more detail about each test:

```bash
python -m pytest tests/ -v
```

The tests cover:

- Streak calculations for daily and weekly habits
- Filtering habits by periodicity
- Saving and loading habits from JSON
- Archiving habits and ID generation

---

## Sample Data

The file `tests/fixtures/habit_fixture.json` contains 5 predefined habits with 4 weeks of completion history. This file is used by the tests and also by the app if you point it there. By default, the app stores your own data in `data/habits.json`, which is created automatically on the first run.

---

## Notes

- Habit data is stored as plain JSON, so you can open and read it in any text editor
- Completing a habit more than once in the same day (or week for weekly habits) still only counts as one period for streak purposes
- Archived habits are not counted in analytics or streak comparisons
