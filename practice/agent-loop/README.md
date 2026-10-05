# agent-loop — минимальный агент на Anthropic Python SDK

> **Необязательный материал** модуля 09 (упражнение ⭐). Нужен, чтобы своими глазами увидеть, что Claude Code «под капотом» — это цикл из запросов к модели и вызовов tools.

## ⚠️ Прежде чем начать

- **Это платно.** Скрипт ходит в Anthropic API напрямую. Оплата API отдельна от подписки Claude Pro/Max: нужен аккаунт на https://console.anthropic.com с балансом. Один запуск — обычно несколько запросов по несколько тысяч tokens, то есть копейки/центы, но **следите за расходом** в консоли.
- **Нужен API key.** Ключ — это пароль к вашему счёту. Никогда не вставляйте его в код, в чат с Claude и не коммитьте в git. Храните в переменной окружения (env var).
- **Скрипт видит только текущую папку.** Функция `safe_path` не даёт выйти выше. Всё равно запускайте его в учебной папке, а не в домашней.

## Установка

```bash
cd ~/claude-practice/agent-loop
python -m venv .venv
```

Активировать venv — Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```
macOS / Linux:
```bash
source .venv/bin/activate
```

Затем:
```bash
pip install anthropic
```

## Ключ в переменную окружения (только на текущее окно терминала)

Windows PowerShell:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```
macOS / Linux:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

> **Почему так?** Переменная окружения живёт в памяти терминала и исчезает при закрытии окна. Ключ не попадёт ни в файл, ни в git, ни в историю чата.

Модель можно сменить переменной `CLAUDE_MODEL` (актуальные id — https://docs.claude.com/en/docs/about-claude/models).

## Запуск

```bash
python agent.py "Что лежит в этой папке и о чём файл README.md?"
```

Вы увидите шаги цикла:

```
--- шаг 1: stop_reason=tool_use, tokens in/out=...
[tool] list_dir({'path': '.'})
--- шаг 2: stop_reason=tool_use, ...
[tool] read_file({'path': 'README.md'})
--- шаг 3: stop_reason=end_turn, ...
<итоговый ответ>
```

## Как читать код

1. `TOOLS` — описания инструментов. Модель видит **только их**, не код функций.
2. `run_tool` — наш код, который реально выполняет действие. Модель сама ничего не выполняет: она лишь *просит*.
3. Цикл в `main`: пока `stop_reason == "tool_use"` — выполняем tool, добавляем в `messages` ответ модели и результат, отправляем всё заново.
4. `messages` растёт с каждым шагом — это и есть context window агента. Обратите внимание на `tokens in`: он увеличивается.
