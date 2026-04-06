from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Dict, Iterable, List, Optional, Tuple


PRIORITY_ORDER: Dict[str, int] = {"low": 1, "medium": 2, "high": 3}


def _time_to_minutes(time_str: str) -> int:
    """Convert a HH:MM time string to minutes since midnight."""
    parsed = datetime.strptime(time_str, "%H:%M")
    return parsed.hour * 60 + parsed.minute


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    time_str: str
    frequency: Optional[str] = None
    notes: Optional[str] = None
    completed: bool = False
    due_date: date = field(default_factory=date.today)
    pet_name: Optional[str] = None

    def update_details(
        self,
        title: Optional[str] = None,
        duration_minutes: Optional[int] = None,
        priority: Optional[str] = None,
        time_str: Optional[str] = None,
        frequency: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Update any provided task fields in place."""
        if title is not None:
            self.title = title
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if priority is not None:
            self.priority = priority
        if time_str is not None:
            self.time_str = time_str
        if frequency is not None:
            self.frequency = frequency
        if notes is not None:
            self.notes = notes

    def estimate_time(self) -> int:
        """Return the task duration in minutes."""
        return self.duration_minutes

    def describe(self) -> str:
        """Return a human-readable description of the task."""
        parts = [
            f"{self.title} at {self.time_str}",
            f"{self.duration_minutes} min",
            f"priority: {self.priority}",
        ]
        if self.pet_name:
            parts.append(f"pet: {self.pet_name}")
        if self.frequency:
            parts.append(f"freq: {self.frequency}")
        if self.completed:
            parts.append("completed")
        return " (" + ", ".join(parts) + ")"

    def time_minutes(self) -> int:
        """Return minutes since midnight for sorting."""
        return _time_to_minutes(self.time_str)

    def mark_complete(self) -> Optional[Task]:
        """Mark complete and return a new recurring task if needed."""
        self.completed = True
        if self.frequency is None:
            return None

        frequency_normalized = self.frequency.lower()
        if frequency_normalized == "daily":
            delta = timedelta(days=1)
        elif frequency_normalized == "weekly":
            delta = timedelta(days=7)
        else:
            return None

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            time_str=self.time_str,
            frequency=self.frequency,
            notes=self.notes,
            completed=False,
            due_date=self.due_date + delta,
            pet_name=self.pet_name,
        )

    def is_due_on(self, target_date: date) -> bool:
        """Return True if the task is due on the target date."""
        return self.due_date == target_date


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    notes: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def list_tasks(
        self,
        completed: Optional[bool] = None,
        due_date: Optional[date] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion or due date."""
        tasks = self.tasks
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        if due_date is not None:
            tasks = [task for task in tasks if task.is_due_on(due_date)]
        return tasks

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and append a recurring follow-up."""
        new_task = task.mark_complete()
        if new_task is not None:
            self.tasks.append(new_task)
        return new_task


class Owner:
    def __init__(
        self,
        name: str,
        available_time_minutes: int,
        preferences: Optional[dict] = None,
    ) -> None:
        """Create an owner who manages pets and tasks."""
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.preferences = preferences or {}
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Add an owner-level task (not tied to a specific pet)."""
        self.tasks.append(task)

    def set_preferences(self, preferences: dict) -> None:
        """Replace owner preferences with new values."""
        self.preferences = preferences

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across owner and pets."""
        pet_tasks = [task for pet in self.pets for task in pet.tasks]
        return self.tasks + pet_tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Initialize a scheduler for the owner."""
        self.owner = owner

    def sort_by_time(self, tasks: Iterable[Task]) -> List[Task]:
        """Return tasks sorted by time and priority."""
        return sorted(
            tasks,
            key=lambda task: (
                task.time_minutes(),
                -PRIORITY_ORDER.get(task.priority, 0),
            ),
        )

    def filter_tasks(
        self,
        tasks: Iterable[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        filtered = list(tasks)
        if pet_name is not None:
            filtered = [task for task in filtered if task.pet_name == pet_name]
        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]
        return filtered

    def tasks_for_date(self, target_date: date) -> List[Task]:
        """Return tasks due on the target date."""
        return [task for task in self.owner.get_all_tasks() if task.is_due_on(target_date)]

    def detect_conflicts(self, tasks: Iterable[Task]) -> List[str]:
        """Return warnings for tasks that share the same time."""
        buckets: Dict[Tuple[str, date], List[Task]] = {}
        for task in tasks:
            key = (task.time_str, task.due_date)
            buckets.setdefault(key, []).append(task)

        warnings: List[str] = []
        for (time_str, due_date), bucket in buckets.items():
            if len(bucket) > 1:
                task_titles = ", ".join(task.title for task in bucket)
                warnings.append(
                    f"Conflict at {time_str} on {due_date.isoformat()}: {task_titles}"
                )
        return warnings

    def build_daily_plan(self, target_date: date) -> Tuple[List[Task], List[str]]:
        """Select tasks that fit in available time and return warnings."""
        tasks = self.tasks_for_date(target_date)
        tasks = self.filter_tasks(tasks, completed=False)
        sorted_tasks = self.sort_by_time(tasks)

        selected: List[Task] = []
        used_minutes = 0
        for task in sorted_tasks:
            if used_minutes + task.duration_minutes <= self.owner.available_time_minutes:
                selected.append(task)
                used_minutes += task.duration_minutes

        warnings = self.detect_conflicts(sorted_tasks)
        if used_minutes < self.owner.available_time_minutes:
            warnings.append(
                f"You have {self.owner.available_time_minutes - used_minutes} free minutes."
            )

        return selected, warnings

    def explain_plan(self, tasks: Iterable[Task]) -> List[str]:
        """Return a list of brief explanations for chosen tasks."""
        explanations = []
        for task in tasks:
            explanations.append(
                f"{task.title} scheduled at {task.time_str} because it is {task.priority} priority."
            )
        return explanations
