"""Command-line task manager."""

import argparse
from pathlib import Path

from laba8.data import TaskRepository
from laba8.service import TaskService


def build_parser() -> argparse.ArgumentParser:
    """Create a parser for task commands."""
    parser = argparse.ArgumentParser(
        description="Task manager with JSON storage"
    )

    parser.add_argument(
        "--file",
        type=Path,
        default=Path("tasks.json"),
        help="Path to the JSON file"
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True
    )

    add_parser = commands.add_parser("add", help="Add a task")
    add_parser.add_argument("title", help="Task title")

    commands.add_parser("list", help="Show all tasks")

    done_parser = commands.add_parser("done", help="Complete a task")
    done_parser.add_argument("id", type=int, help="Task ID")

    return parser


def main() -> None:
    """Execute a task command."""
    parser = build_parser()
    args = parser.parse_args()

    service = TaskService(TaskRepository(args.file))

    try:
        if args.command == "add":
            task = service.add_task(args.title)
            print(f"Added #{task['id']}: {task['title']}")

        elif args.command == "list":
            tasks = service.list_tasks()

            if not tasks:
                print("No tasks yet.")

            for task in tasks:
                status = "x" if task["done"] else " "
                print(f"{task['id']}. [{status}] {task['title']}")

        elif args.command == "done":
            task = service.complete_task(args.id)
            print(f"Completed #{task['id']}: {task['title']}")

    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
