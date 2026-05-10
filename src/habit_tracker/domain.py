"""Domain entities for the habit tracker."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class Periodicity(Enum):
    """Supported habit periodicities."""

    DAILY = "daily"
    WEEKLY = "weekly"

    @classmethod
    def from_value(cls, value: Any) -> "Periodicity":
        """Convert a string or enum value to Periodicity."""
        if isinstance(value, cls):
            return value

        normalized = str(value).strip().lower()

        for member in cls:
            if member.value == normalized or member.name.lower() == normalized:
                return member

        raise ValueError("Periodicity must be 'daily' or 'weekly'.")


@dataclass
class Habit:
    """Represents a habit and its completion history."""

    id: str
    name: str
    periodicity: Periodicity
    created_at: datetime
    completions: List[datetime] = field(default_factory=list)
    archived: bool = False
    notes: str = ""

    def mark_complete(self, timestamp: Optional[datetime] = None) -> None:
        """Record a completion timestamp for the habit."""
        self.completions.append(timestamp or datetime.utcnow())
        self.completions.sort()

    def rename(self, new_name: str) -> None:
        """Rename the habit."""
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("Habit name cannot be empty.")
        self.name = new_name

    def set_periodicity(self, periodicity: Any) -> None:
        """Update the habit periodicity."""
        self.periodicity = Periodicity.from_value(periodicity)

    def archive(self) -> None:
        """Archive the habit."""
        self.archived = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert the habit to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "periodicity": self.periodicity.value,
            "created_at": self.created_at.isoformat(),
            "completions": [completion.isoformat() for completion in self.completions],
            "archived": self.archived,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Habit":
        """Create a Habit object from a dictionary."""
        return cls(
            id=str(payload["id"]),
            name=str(payload["name"]),
            periodicity=Periodicity.from_value(payload["periodicity"]),
            created_at=_parse_datetime(payload["created_at"]),
            completions=[
                _parse_datetime(timestamp)
                for timestamp in payload.get("completions", [])
            ],
            archived=bool(payload.get("archived", False)),
            notes=str(payload.get("notes", "")),
        )


def _parse_datetime(value: Any) -> datetime:
    """Parse an ISO 8601 datetime string."""
    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        raise TypeError("Datetime must be a datetime object or ISO string.")

    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)