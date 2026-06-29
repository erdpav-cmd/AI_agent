import json
import os
from datetime import datetime
from pathlib import Path

import telebot
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from agent.agent import get_agent

load_dotenv()

MEMORY_DIR = Path("memory")
MEMORY_DIR.mkdir(exist_ok=True)
TELEGRAM_MAX_MESSAGE_LENGTH = 4096

agent = get_agent()
chat_histories: dict[int, list] = {}


def _get_bot() -> telebot.TeleBot:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("Укажите BOT_TOKEN в файле .env")
    return telebot.TeleBot(token)


bot = _get_bot()


def _memory_path(chat_id: int) -> Path:
    return MEMORY_DIR / f"{chat_id}.json"


def _load_memory(chat_id: int) -> list:
    path = _memory_path(chat_id)
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save_memory(chat_id: int, memory: list) -> None:
    with open(_memory_path(chat_id), "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)


def _get_chat_history(chat_id: int) -> list:
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []
    return chat_histories[chat_id]


def _invoke_agent(chat_id: int, user_input: str) -> str:
    history = _get_chat_history(chat_id)
    response = agent.invoke({
        "messages": history + [HumanMessage(content=user_input)]
    })
    agent_output = next(
        msg.content
        for msg in reversed(response["messages"])
        if isinstance(msg, AIMessage) and msg.content
    )
    history.extend([
        HumanMessage(content=user_input),
        AIMessage(content=agent_output),
    ])
    memory = _load_memory(chat_id)
    memory.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "agent": agent_output,
    })
    _save_memory(chat_id, memory)
    return agent_output


def _send_long_message(chat_id: int, text: str) -> None:
    for i in range(0, len(text), TELEGRAM_MAX_MESSAGE_LENGTH):
        bot.send_message(chat_id, text[i:i + TELEGRAM_MAX_MESSAGE_LENGTH])


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message) -> None:
    bot.reply_to(
        message,
        "Привет! Я AI-агент.\n\n"
        "Могу искать информацию в интернете, узнавать погоду, курсы валют и криптовалют, "
        "работать с файлами и генерировать QR-коды.\n\n"
        "Команды:\n"
        "/clear — очистить историю диалога",
    )


@bot.message_handler(commands=["clear"])
def clear_history(message: telebot.types.Message) -> None:
    chat_id = message.chat.id
    chat_histories[chat_id] = []
    bot.reply_to(message, "История диалога очищена.")


@bot.message_handler(content_types=["text"])
def handle_message(message: telebot.types.Message) -> None:
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, "typing")
    try:
        output = _invoke_agent(chat_id, message.text)
        _send_long_message(chat_id, output)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


def main() -> None:
    print("Telegram-бот запущен. Нажмите Ctrl+C для остановки.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
