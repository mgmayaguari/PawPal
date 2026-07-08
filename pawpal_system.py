from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    task_id: int
    description: str
    time: str
    frequency: str = "once"
    completed: bool = False
    status: str = "pending"
    pet: Optional["Pet"] = None

    def edit_task(self, **kwargs) -> None:
        """Update task details."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        if self.completed:
            self.status = "completed"
        else:
            self.status = "pending"

    def delete_task(self) -> None:
        """Remove the task from its pet."""
        if self.pet is not None:
            self.pet.tasks = [task for task in self.pet.tasks if task is not self]
        self.pet = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task complete and create the next recurring occurrence when needed."""
        self.completed = True
        self.status = "completed"

        if self.frequency in {"daily", "weekly"} and self.pet is not None:
            next_task = Task(
                task_id=self.task_id + 1000,
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                completed=False,
                status="pending",
                pet=self.pet,
            )
            self.pet.add_task(next_task)
            return next_task

        return None


@dataclass
class Pet:
    pet_id: int
    name: str
    age: Optional[int] = None
    birth_date: Optional[str] = None
    breed: Optional[str] = None
    species: str = "other"
    owner: Optional["Owner"] = None
    tasks: List[Task] = field(default_factory=list)

    def update_pet_info(self, **kwargs) -> None:
        """Update pet details."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def add_task(self, task: Task) -> None:
        """Attach a task to the pet."""
        if task in self.tasks:
            return
        task.pet = self
        self.tasks.append(task)


@dataclass
class Owner:
    owner_id: int
    name: str
    join_date: Optional[str] = None
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        if pet in self.pets:
            return
        pet.owner = self
        self.pets.append(pet)

    def schedule_task(self, task: Task, pet: Optional[Pet] = None) -> None:
        """Schedule a task for one of the owner's pets."""
        target_pet = pet or (self.pets[0] if self.pets else None)
        if target_pet is None:
            return
        target_pet.add_task(task)

    def view_schedule(self) -> List[Task]:
        """Return all tasks for the owner."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_all_tasks(self) -> List[Task]:
        """Return every task across the owner's pets."""
        return self.view_schedule()

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return tasks that match the given completion status and/or pet name."""
        tasks = self.get_all_tasks()

        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]

        if pet_name is not None:
            normalized_pet_name = pet_name.strip().lower()
            tasks = [
                task
                for task in tasks
                if task.pet is not None and normalized_pet_name in task.pet.name.lower()
            ]

        return tasks


@dataclass
class Scheduler:
    owner: Optional[Owner] = None
    pet: Optional[Pet] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Register a task with the scheduler."""
        if task in self.tasks:
            return

        if task.pet is not None:
            task.pet.add_task(task)
        elif self.pet is not None:
            self.pet.add_task(task)
        elif self.owner is not None:
            self.owner.schedule_task(task)

        if task not in self.tasks:
            self.tasks.append(task)

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by time using a lambda key for HH:MM values."""
        tasks_to_sort = list(tasks) if tasks is not None else []
        if not tasks_to_sort:
            if self.pet is not None:
                tasks_to_sort = list(self.pet.tasks)
            elif self.owner is not None:
                tasks_to_sort = self.owner.get_all_tasks()
            else:
                tasks_to_sort = list(self.tasks)

        return sorted(
            tasks_to_sort,
            key=lambda task: tuple(int(part) for part in task.time.split(":")),
        )

    def view_schedule(self) -> List[Task]:
        """Return the scheduled tasks sorted by time."""
        all_tasks = list(self.tasks)
        if self.pet is not None:
            all_tasks = list(self.pet.tasks)
        elif self.owner is not None:
            all_tasks = self.owner.get_all_tasks()

        return self.sort_by_time(all_tasks)

    def check_conflicts(self) -> str:
        """Return a lightweight warning message when tasks share the same time."""
        all_tasks = list(self.tasks)
        if self.pet is not None:
            all_tasks = list(self.pet.tasks)
        elif self.owner is not None:
            all_tasks = self.owner.get_all_tasks()

        seen_times: dict[str, List[Task]] = {}

        for task in all_tasks:
            if task.time not in seen_times:
                seen_times[task.time] = []
            seen_times[task.time].append(task)

        for time_value, tasks_at_same_time in seen_times.items():
            if len(tasks_at_same_time) > 1:
                pet_names = ", ".join(sorted({task.pet.name for task in tasks_at_same_time if task.pet is not None}))
                return f"Warning: {len(tasks_at_same_time)} tasks overlap at {time_value} for {pet_names or 'unassigned pets'}."

        return "No conflicts detected."
