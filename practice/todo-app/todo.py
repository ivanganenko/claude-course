"""todo — маленький менеджер задач для командной строки.

Примеры:
    python todo.py add "Отправить счёт" --priority high --due 2026-10-15
    python todo.py list
    python todo.py list --all
    python todo.py done 3
    python todo.py delete 3
    python todo.py stats
"""

import argparse
import sys
from datetime import date

from models import PRIORITIES, Task, next_id, sort_tasks
from storage import load_tasks, save_tasks


def parse_due(value: str) -> str:
    """Проверить, что срок задан в формате YYYY-MM-DD (используется argparse)."""
    try:
        date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"неверная дата '{value}', нужен формат YYYY-MM-DD")
    return value


def find_task(tasks: list[Task], task_id: int) -> Task | None:
    """Найти задачу по id. Если такой нет — вернуть None."""
    for task in tasks:
        if task.id == task_id:
            return task
    return None


def format_task(task: Task) -> str:
    """Одна строка для вывода задачи в терминал."""
    mark = "x" if task.done else " "
    due = f"  до {task.due}" if task.due else ""
    overdue = "  (просрочено!)" if task.is_overdue() else ""
    return f"[{mark}] {task.id:>3}  {task.priority:<6}  {task.title}{due}{overdue}"


def cmd_add(args: argparse.Namespace) -> int:
    """Добавить новую задачу."""
    tasks = load_tasks()
    task = Task(id=next_id(tasks), title=args.title, priority=args.priority, due=args.due)
    tasks.append(task)
    save_tasks(tasks)
    print(f"Добавлена задача {task.id}: {task.title}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """Показать задачи. Выполненные — только с флагом --all."""
    tasks = load_tasks()
    if not args.all:
        tasks = [t for t in tasks if not t.done]
    if not tasks:
        print("Задач нет.")
        return 0
    for task in sort_tasks(tasks):
        print(format_task(task))
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    """Отметить задачу выполненной."""
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        print(f"Задача {args.id} не найдена.", file=sys.stderr)
        return 1
    task.done = True
    save_tasks(tasks)
    print(f"Выполнено: {task.title}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    """Удалить задачу."""
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        print(f"Задача {args.id} не найдена.", file=sys.stderr)
        return 1
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Удалена задача {task.id}: {task.title}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    """Показать сводку по задачам."""
    tasks = load_tasks()
    done = sum(1 for t in tasks if t.done)
    overdue = sum(1 for t in tasks if t.is_overdue())
    print(f"Всего задач:  {len(tasks)}")
    print(f"Выполнено:    {done}")
    print(f"Осталось:     {len(tasks) - done}")
    print(f"Просрочено:   {overdue}")
    print("Невыполненные по приоритету:")
    for priority in PRIORITIES:
        count = sum(1 for t in tasks if t.priority == priority and not t.done)
        print(f"  {priority:<6} {count}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Описать команды и аргументы командной строки."""
    parser = argparse.ArgumentParser(prog="todo", description="Простой менеджер задач.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="добавить задачу")
    p.add_argument("title", help="текст задачи")
    p.add_argument("--priority", choices=PRIORITIES, default="medium")
    p.add_argument("--due", type=parse_due, help="срок, YYYY-MM-DD")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="показать задачи")
    p.add_argument("--all", action="store_false", help="показать и выполненные задачи")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("done", help="отметить задачу выполненной")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("delete", help="удалить задачу")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("stats", help="сводка по задачам")
    p.set_defaults(func=cmd_stats)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Точка входа: разобрать аргументы и выполнить команду."""
    # Чтобы кириллица печаталась корректно в любом терминале Windows.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
