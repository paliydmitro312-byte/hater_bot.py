import random
import os
import requests

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


BOT_TOKEN = os.getenv("BOT_TOKEN")

GITHUB_URL = "https://raw.githubusercontent.com/paliydmitro312-byte/hater_bot.py/main/hater_bot.py"


def get_phrases():
    response = requests.get(GITHUB_URL, timeout=10)
    response.raise_for_status()

    text = response.text

    start = text.find("PHRASES = [")
    end = text.find("]", start)

    if start == -1 or end == -1:
        raise ValueError("Не найден список PHRASES")

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

        await update.message.reply_text(random.choice(phrases))

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
