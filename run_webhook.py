from flask import Flask, request
from aiogram import Bot, Dispatcher, types
import os
import asyncio

API_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

app = Flask(__name__)

# Настройка webhook Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = types.Update.to_object(request.get_json())
    asyncio.run(dp.process_update(update))
    return "OK"

if __name__ == "__main__":
    # Устанавливаем webhook на Railway URL после деплоя
    print(f"Flask запущен на 0.0.0.0:{PORT}")
    app.run(host="0.0.0.0", port=PORT)
