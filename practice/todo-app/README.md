# todo-app

Маленький менеджер задач для командной строки на Python. Задачи хранятся в файле `todos.json`.

## Требования

- Python 3.11 или новее (`python --version`)
- Для тестов — `pytest` (см. ниже)

## Запуск

Внешних зависимостей нет — достаточно Python.

```bash
python todo.py list                 # невыполненные задачи
python todo.py list --all           # все задачи, включая выполненные
python todo.py add "Позвонить поставщику" --priority high --due 2026-10-15
python todo.py done 2               # отметить задачу 2 выполненной
python todo.py delete 2             # удалить задачу 2
python todo.py stats                # сводка
python todo.py --help               # справка
```

На macOS/Linux вместо `python` может понадобиться `python3`.

Приоритеты: `low`, `medium` (по умолчанию), `high`. Срок (`--due`) — дата в формате `YYYY-MM-DD`.

## Где хранятся данные

По умолчанию — `todos.json` в текущей папке. Другой файл можно задать переменной окружения `TODO_FILE`:

```powershell
# Windows PowerShell
$env:TODO_FILE = "work.json"; python todo.py list
```

```bash
# macOS / Linux / Git Bash
TODO_FILE=work.json python todo.py list
```

## Тесты

Рекомендуется виртуальное окружение (venv), чтобы pytest не попал в системный Python:

```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

## Структура

| Файл | Что внутри |
|------|-----------|
| `todo.py` | команды CLI (argparse) и вывод в терминал |
| `models.py` | dataclass `Task`, генерация id, сортировка |
| `storage.py` | чтение и запись `todos.json` |
| `todos.json` | пример данных |
| `tests/` | тесты pytest |
