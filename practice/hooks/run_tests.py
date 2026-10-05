"""Hook PostToolUse: запускать тесты после того, как Claude изменил Python-файл (модуль 10, упражнение 3).

Как подключить (в .claude/settings.json проекта):
    {"hooks": {"PostToolUse": [{"matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python .claude/hooks/run_tests.py"}]}]}}

Идея: правка уже сделана (PostToolUse = «после»), отменить её нельзя. Но мы можем сразу
прогнать pytest и, если тесты упали, вернуть exit code 2 — тогда текст из stderr увидит Claude
и сможет починить свою правку. Точное поведение exit 2 для PostToolUse проверьте в docs:
https://code.claude.com/docs (раздел о hooks).

Проверить вручную, из папки проекта:
    echo '{"tool_name":"Edit","tool_input":{"file_path":"todo.py"}}' | python .claude/hooks/run_tests.py
    Код выхода: PowerShell `$LASTEXITCODE`, bash `echo $?`.
"""
import json
import subprocess
import sys

TIMEOUT_SECONDS = 60  # тесты не должны «вешать» сессию Claude


def should_run(file_path: str) -> bool:
    """Решить, нужно ли запускать тесты для этого файла."""
    # TODO 1: запускать тесты только при изменении .py файлов.
    # Почему не всегда? Подумайте, что будет при правке README.md или todos.json.
    return True


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    file_path = event.get("tool_input", {}).get("file_path", "")
    if not should_run(file_path):
        return 0

    # sys.executable — тот же Python, которым запущен hook (важно на Windows и с venv).
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--no-header"],
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"Тесты не уложились в {TIMEOUT_SECONDS} с.", file=sys.stderr)
        return 1  # неблокирующая ошибка: сообщаем, но не мешаем работе

    if result.returncode != 0:
        # TODO 2: тесты упали. Выведите в stderr последние ~30 строк result.stdout
        # (там имена упавших тестов и причины) с короткой пометкой для Claude,
        # и верните 2, чтобы Claude увидел этот текст.
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
