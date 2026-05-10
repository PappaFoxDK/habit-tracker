import sys
from pathlib import Path

# Add the src/ folder to the path so tests can import habit_tracker directly.
sys.path.insert(0, str(Path(__file__).parent / "src"))