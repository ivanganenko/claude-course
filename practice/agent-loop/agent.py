"""Минимальный agent loop на Anthropic Python SDK (модуль 09, необязательное упражнение).

Что делает: даёт модели два tools — list_dir и read_file — и крутит цикл
«модель думает → просит вызвать tool → мы выполняем → отдаём результат → повторяем»,
пока модель не ответит текстом без запроса tool.

Запуск (нужен ANTHROPIC_API_KEY, запросы ПЛАТНЫЕ — см. README.md):
    python agent.py "Что лежит в этой папке и о чём файл README.md?"
"""
import os
import sys
from pathlib import Path

import anthropic

# Алиас модели. Проверьте актуальный id в docs:
# https://docs.claude.com/en/docs/about-claude/models
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")
MAX_TURNS = 10            # предохранитель: агент не может крутиться бесконечно (и тратить деньги)
ROOT = Path.cwd().resolve()  # агенту доступна только текущая папка и всё внутри неё

# Описание tools для модели. Модель НЕ видит код функций — только name, description и схему.
# Поэтому description пишем так, будто объясняем коллеге, когда и зачем звать этот tool.
TOOLS = [
    {
        "name": "list_dir",
        "description": "Показать файлы и папки по относительному пути. Используй, чтобы понять структуру проекта.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Путь относительно рабочей папки, например '.'"}},
            "required": ["path"],
        },
    },
    {
        "name": "read_file",
        "description": "Прочитать текстовый файл целиком (до 20 000 символов). Используй, когда нужно содержимое файла.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Путь к файлу относительно рабочей папки"}},
            "required": ["path"],
        },
    },
]


def safe_path(rel: str) -> Path:
    """Не выпускаем агента за пределы ROOT (защита от '../../секреты')."""
    p = (ROOT / rel).resolve()
    if p != ROOT and ROOT not in p.parents:
        raise ValueError(f"путь {rel!r} вне рабочей папки")
    return p


def run_tool(name: str, args: dict) -> str:
    """Выполнить tool и вернуть результат строкой. Ошибку тоже возвращаем модели — пусть она её «увидит»."""
    try:
        if name == "list_dir":
            items = sorted(safe_path(args["path"]).iterdir())
            return "\n".join(f"{'[dir] ' if i.is_dir() else ''}{i.name}" for i in items) or "(пусто)"
        if name == "read_file":
            return safe_path(args["path"]).read_text(encoding="utf-8")[:20_000]
        return f"Ошибка: неизвестный tool {name}"
    except Exception as e:  # noqa: BLE001 — для учебного примера ловим всё
        return f"Ошибка: {e}"


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Не задан ANTHROPIC_API_KEY. Как его задать — см. README.md.")
    task = " ".join(sys.argv[1:]) or "Опиши, что лежит в этой папке."
    client = anthropic.Anthropic()  # ключ берётся из переменной окружения ANTHROPIC_API_KEY
    messages = [{"role": "user", "content": task}]  # вся «память» агента — этот список

    for turn in range(1, MAX_TURNS + 1):
        response = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages)
        print(f"\n--- шаг {turn}: stop_reason={response.stop_reason}, "
              f"tokens in/out={response.usage.input_tokens}/{response.usage.output_tokens}")

        if response.stop_reason != "tool_use":  # модель закончила — печатаем ответ и выходим
            print("".join(b.text for b in response.content if b.type == "text"))
            return

        # Модель попросила tool(s). Сохраняем её сообщение целиком (вместе с блоками tool_use) —
        # иначе на следующем шаге она «не вспомнит», что именно просила.
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "text":
                print(f"[мысль] {block.text}")
            elif block.type == "tool_use":
                print(f"[tool] {block.name}({block.input})")
                output = run_tool(block.name, block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})
        messages.append({"role": "user", "content": results})  # результаты tools уходят как сообщение user

    print(f"\nОстановлено: достигнут лимит MAX_TURNS={MAX_TURNS}.")


if __name__ == "__main__":
    main()
