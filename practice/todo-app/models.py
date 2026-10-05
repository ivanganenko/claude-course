"""Модель данных: задача (Task) и вспомогательные функции для списка задач."""

from dataclasses import asdict, dataclass, field
from datetime import date, datetime

# Допустимые приоритеты задачи — от наименее к наиболее важному.
PRIORITIES = ("low", "medium", "high")


def _now() -> str:
    """Вернуть текущее время в формате ISO 8601 без микросекунд."""
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class Task:
    """Одна задача в списке дел."""

    id: int
    title: str
    priority: str = "medium"
    due: str | None = None  # срок в формате YYYY-MM-DD или None
    done: bool = False
    created_at: str = field(default_factory=_now)

    def is_overdue(self, today: date | None = None) -> bool:
        """True, если срок уже прошёл, а задача ещё не выполнена."""
        if self.done or self.due is None:
            return False
        today = today or date.today()
        return date.fromisoformat(self.due) < today

    def to_dict(self) -> dict:
        """Превратить задачу в словарь для сохранения в JSON."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Создать задачу из словаря, прочитанного из JSON."""
        return cls(**data)


def next_id(tasks: list[Task]) -> int:
    """Вернуть id для новой задачи."""
    return len(tasks) + 1


def sort_tasks(tasks: list[Task]) -> list[Task]:
    """Отсортировать задачи: сначала самые важные, внутри приоритета — по сроку.

    Задачи без срока идут в конце своей группы.
    """
    return sorted(tasks, key=lambda t: (t.priority, t.due or "9999-12-31"))
