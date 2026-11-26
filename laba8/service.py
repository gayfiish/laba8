"""Service layer for managing tasks."""

from typing import Any

from laba8.data import TaskRepository


class TaskService:
    """Manage tasks using a repository."""

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def add_task(self, title: str) -> dict[str, Any]:
        """Validate and save a new task."""
        title = title.strip()

        if not title:
            raise ValueError("Task title cannot be empty")

        tasks = self.repository.load()
        next_id = max((int(task["id"]) for task in tasks), default=0) + 1

        task = {"id": next_id, "title": title, "done": False}
        tasks.append(task)
        self.repository.save(tasks)

        return task

    def list_tasks(self) -> list[dict[str, Any]]:
        """Return all saved tasks."""
        return self.repository.load()

    def complete_task(self, task_id: int) -> dict[str, Any]:
        """Mark an existing task as completed."""
        if task_id < 1:
            raise ValueError("Task ID must be positive")

        tasks = self.repository.load()

        for task in tasks:
            if task["id"] == task_id:
                if task["done"]:
                    raise ValueError("Task is already completed")

                task["done"] = True
                self.repository.save(tasks)
                return task

        raise ValueError(f"Task #{task_id} not found")
