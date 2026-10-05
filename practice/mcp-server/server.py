"""MCP server «notes»: даёт Claude доступ к папке с заметками в формате Markdown.

Запуск вручную (для проверки, что нет ошибок импорта):
    python server.py
Сервер общается через stdio (stdin/stdout), поэтому после запуска он просто
«молчит» и ждёт сообщений от клиента. Остановить — Ctrl+C.

Обычно его запускает сам Claude Code — см. README.md.
"""

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Папка с заметками: переменная окружения NOTES_DIR или ./notes рядом с этим файлом.
# Путь считаем от __file__, а не от текущей папки: Claude Code может запустить
# сервер из любой рабочей директории.
NOTES_DIR = Path(os.environ.get("NOTES_DIR", Path(__file__).parent / "notes"))

# Имя сервера — так он будет виден клиенту.
mcp = FastMCP("notes")


@mcp.tool()
def list_notes() -> list[str]:
    """Вернуть список всех заметок (имена файлов без расширения .md), по алфавиту.

    Используй, чтобы узнать, какие заметки существуют, прежде чем читать одну из них.
    """
    return sorted(path.stem for path in NOTES_DIR.glob("*.md"))


# TODO (упражнение 08.2): добавь tool read_note(name: str) -> str,
#   который возвращает текст заметки по имени (без .md).
#   - Напиши понятный docstring: модель читает его, чтобы решить, когда звать tool.
#   - Подумай о безопасности: что будет, если name = "../../secret"?
#   - Что вернуть, если заметки нет? (подсказка: понятное сообщение об ошибке)

# TODO (упражнение 08.3): добавь третий tool (например, search_notes(query: str))
#   и resource "notes://{name}" через @mcp.resource(...).


# Важно: никаких print() в stdout — stdout занят протоколом MCP.
# Для отладочных сообщений используй print(..., file=sys.stderr).

if __name__ == "__main__":
    mcp.run()  # по умолчанию transport = stdio
