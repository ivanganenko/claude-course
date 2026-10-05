"""Простые тесты модели Task — отправная точка для своих тестов."""

from datetime import date

from models import Task


def test_task_is_overdue_when_due_date_passed():
    task = Task(id=1, title="Сдать отчёт", due="2026-01-10")
    assert task.is_overdue(today=date(2026, 1, 11)) is True
    assert task.is_overdue(today=date(2026, 1, 10)) is False


def test_done_task_is_never_overdue():
    task = Task(id=1, title="Сдать отчёт", due="2026-01-10", done=True)
    assert task.is_overdue(today=date(2030, 1, 1)) is False


def test_task_survives_round_trip_to_dict():
    task = Task(id=7, title="Позвонить поставщику", priority="high", due="2026-03-01")
    assert Task.from_dict(task.to_dict()) == task
