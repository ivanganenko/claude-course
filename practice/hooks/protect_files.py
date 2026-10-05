"""Hook PreToolUse: запретить Claude редактировать защищённые файлы (модуль 10, упражнение 2).

Как подключить (в .claude/settings.json проекта):
    {"hooks": {"PreToolUse": [{"matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python .claude/hooks/protect_files.py"}]}]}}
(на macOS/Linux, возможно, нужно `python3` вместо `python`)

Как это работает:
- Claude Code перед вызовом tool Edit/Write запускает этот скрипт и передаёт на stdin JSON,
  например: {"tool_name": "Edit", "tool_input": {"file_path": "/.../todos.json", ...}, ...}
- exit code 0  -> действие разрешено;
- exit code 2  -> действие ЗАБЛОКИРОВАНО, текст из stderr увидит Claude (и поймёт, почему);
- другой код   -> неблокирующая ошибка самого hook.

Проверить вручную, без Claude (одинарные кавычки работают и в PowerShell, и в bash):
    echo '{"tool_name":"Edit","tool_input":{"file_path":"todos.json"}}' | python protect_files.py
    Затем посмотрите код выхода: PowerShell `$LASTEXITCODE`, bash `echo $?`.
"""
import json
import sys
from pathlib import Path

# TODO 1: перечислите имена файлов, которые Claude трогать нельзя.
# Подумайте: почему сравнивать по имени файла (Path(...).name), а не по полному пути?
PROTECTED_NAMES: set[str] = set()


def is_protected(file_path: str) -> bool:
    """Вернуть True, если файл защищён."""
    # TODO 2: сравните имя файла из file_path с PROTECTED_NAMES.
    # Подсказка: Path(file_path).name даёт "todos.json" из "C:\\...\\todo-app\\todos.json".
    return False


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Не смогли разобрать вход — не ломаем работу Claude, просто пропускаем.
        return 0

    file_path = event.get("tool_input", {}).get("file_path", "")
    if file_path and is_protected(file_path):
        # TODO 3: напишите в stderr понятное объяснение ДЛЯ CLAUDE: что запрещено и что делать вместо этого
        # (например: «меняй данные через команды todo.py»). Затем верните 2.
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
