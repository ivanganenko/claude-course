# mcp-server — свой MCP server «notes»

Учебный MCP server на Python (FastMCP), который даёт Claude доступ к заметкам из папки `notes/`.
Сейчас в нём один рабочий tool — `list_notes`. Остальное ты допишешь в упражнениях модуля 08.

## Что внутри

| Файл | Зачем |
|------|-------|
| `server.py` | сам сервер: FastMCP, tool `list_notes`, TODO для упражнений |
| `requirements.txt` | зависимость `mcp[cli]` (официальный Python SDK) |
| `notes/*.md` | три заметки с вымышленными данными |

## 1. Установка (один раз)

Создай виртуальное окружение (venv) и поставь зависимости **внутри него**.

```powershell
# Windows PowerShell, в папке mcp-server
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# macOS / Linux, в папке mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Проверь, что сервер стартует без ошибок:

```bash
python server.py
```

Он «зависнет» без вывода — это нормально: сервер ждёт сообщений по stdio. Останови его `Ctrl+C`.

## 2. Подключение к Claude Code

Claude Code должен запускать сервер **тем Python, где установлен `mcp`** — то есть Python из `.venv`.
Поэтому указывай полные пути и к Python, и к `server.py`.

```powershell
# Windows PowerShell (подставь свой путь)
claude mcp add --transport stdio notes -- C:\Users\<имя>\claude-practice\mcp-server\.venv\Scripts\python.exe C:\Users\<имя>\claude-practice\mcp-server\server.py
```

```bash
# macOS / Linux
claude mcp add --transport stdio notes -- ~/claude-practice/mcp-server/.venv/bin/python ~/claude-practice/mcp-server/server.py
```

Всё, что после `--`, — это команда запуска сервера. Проверка:

```bash
claude mcp list        # сервер notes в списке и подключён
```

В сессии Claude Code: `/mcp` — статус серверов и их tools. Tool будет называться `mcp__notes__list_notes`.

## 3. Отладка (необязательно)

`mcp dev server.py` открывает MCP Inspector — веб-интерфейс, где можно вызывать tools руками.
Нужен установленный Node.js. Команды SDK могут меняться — сверяйся с документацией: https://modelcontextprotocol.io

## Частые проблемы

| Симптом | Вероятная причина |
|---------|-------------------|
| `ModuleNotFoundError: mcp` | сервер запущен не тем Python (не из `.venv`) |
| `No module named 'mcp.server.fastmcp'` | установлен `mcp` 2.x; переустанови по `requirements.txt` (там `<2`) |
| сервер в `/mcp` с ошибкой подключения | неверный путь в команде; попробуй запустить ту же команду руками в терминале |
| tool «ломает» протокол | в коде есть `print()` в stdout — пиши в `sys.stderr` |
