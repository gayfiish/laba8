"""Tests for task management and data storage."""

from pathlib import Path

import pytest

from laba8.data import TaskRepository
from laba8.service import TaskService


@pytest.fixture
def task_service(tmp_path: Path) -> TaskService:
    """Create a service with isolated storage."""
    return TaskService(TaskRepository(tmp_path / "tasks.json"))


def test_new_repository_is_empty(task_service: TaskService) -> None:
    assert task_service.list_tasks() == []


def test_add_task(task_service: TaskService) -> None:
    task = task_service.add_task("  Learn Poetry  ")

    assert task == {
        "id": 1,
        "title": "Learn Poetry",
        "done": False
    }
    assert task_service.list_tasks() == [task]


def test_unique_task_ids(task_service: TaskService) -> None:
    task_service.add_task("First")
    second = task_service.add_task("Second")

    assert second["id"] == 2


def test_reject_empty_title(task_service: TaskService) -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        task_service.add_task("   ")


def test_complete_task(task_service: TaskService) -> None:
    task_service.add_task("Write tests")
    completed = task_service.complete_task(1)

    assert completed["done"] is True
    assert task_service.list_tasks()[0]["done"] is True


def test_complete_missing_task(task_service: TaskService) -> None:
    with pytest.raises(ValueError, match="not found"):
        task_service.complete_task(99)


def test_complete_twice(task_service: TaskService) -> None:
    task_service.add_task("Write tests")
    task_service.complete_task(1)

    with pytest.raises(ValueError, match="already completed"):
        task_service.complete_task(1)


def test_reject_invalid_id(task_service: TaskService) -> None:
    with pytest.raises(ValueError, match="positive"):
        task_service.complete_task(0)


def test_persistence(tmp_path: Path) -> None:
    filename = tmp_path / "tasks.json"

    TaskService(TaskRepository(filename)).add_task("Save task")
    restored = TaskService(TaskRepository(filename))

    assert restored.list_tasks()[0]["title"] == "Save task"


def test_invalid_data_structure(tmp_path: Path) -> None:
    filename = tmp_path / "tasks.json"
    filename.write_text('{"bad": true}', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid tasks file"):
        TaskRepository(filename).load()


def test_invalid_json(tmp_path: Path) -> None:
    filename = tmp_path / "tasks.json"
    filename.write_text("invalid json", encoding="utf-8")

    with pytest.raises(ValueError):
        TaskRepository(filename).load()
