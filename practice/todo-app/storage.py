"""Чтение и запись списка задач в JSON-файл."""

import json
import os
from pathlib import Path

from models import Task

DEFAULT_FILE = "todos.json"


def data_path() -> Path:
    """Путь к файлу с задачами: переменная окружения TODO_FILE или ./todos.json."""
    return Path(os.environ.get("TODO_FILE", DEFAULT_FILE))


def load_tasks(path: Path | None = None) -> list[Task]:
    """Прочитать задачи из файла. Если файла ещё нет — вернуть пустой список."""
    path = path or data_path()
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return [Task.from_dict(item) for item in data]


def save_tasks(tasks: list[Task], path: Path | None = None) -> None:
    """Сохранить задачи в файл (перезаписывает его целиком)."""
    path = path or data_path()
    with path.open("w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
        f.write("\n")
