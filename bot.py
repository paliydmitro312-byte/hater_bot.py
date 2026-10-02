import random
import os
import requests

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ссылка на raw-файл hater_bot.py
GIST_URL = "ВСТАВЬ_СЮДА_RAW_ССЫЛКУ"


def get_phrases():
    response = requests.get(GIST_URL, timeout=10)
    response.raise_for_status()

    text = response.text

    start = text.find("PHRASES = [")
    end = text.find("]", start)

    if start == -1 or end == -1:
        raise ValueError("Список PHRASES не найден")

    block = text[start + len("PHRASES = ["):end]

    phrases = []

    for line in block.splitlines():
        line = line.strip()

        if line.startswith(("'", '"')):
            phrase = line.rstrip(",").strip("'\"")

            if phrase:
                phrases.append(phrase)

    return phrases


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😈 Хейтер Кей активирован!\n\n"
        "Напиши /insult — и получишь случайное оскорбление."
    )


async def insult(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        phrases = get_phrases()

        if not phrases:
            await update.message.reply_text("Фразы не найдены 😭")
            return

        phrase = random.choice(phrases)
        await update.message.reply_text(phrase)

    except Exception as error:
        print("Ошибка:", error)
        await update.message.reply_text(
            "Не удалось загрузить фразы 😭"
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("insult", insult))

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
