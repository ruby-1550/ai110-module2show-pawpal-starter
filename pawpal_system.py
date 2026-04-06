from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    frequency: Optional[str] = None
    notes: Optional[str] = None

    def update_details(
        self,
        title: Optional[str] = None,
        duration_minutes: Optional[int] = None,
        priority: Optional[str] = None,
        frequency: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        pass

    def estimate_time(self) -> int:
        pass

    def describe(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    notes: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def list_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(
        self,
        name: str,
        available_time_minutes: int,
        preferences: Optional[dict] = None,
    ) -> None:
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.preferences = preferences or {}
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def set_preferences(self, preferences: dict) -> None:
        pass


class Schedule:
    def __init__(
        self,
        schedule_date: date,
        total_available_minutes: int,
    ) -> None:
        self.date = schedule_date
        self.total_available_minutes = total_available_minutes
        self.selected_tasks: List[Task] = []
        self.rationale: List[str] = []

    def build(self, tasks: List[Task], constraints: Optional[dict] = None) -> None:
        pass

    def prioritize(self, tasks: List[Task]) -> List[Task]:
        pass

    def explain_plan(self) -> str:
        pass
