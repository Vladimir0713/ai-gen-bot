import os
import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from bot import register

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
register(dp)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = types.Update(**request.json)
    asyncio.get_event_loop().run_until_complete(dp.process_update(update))
    return "ok"

@app.route("/")
def index():
    return "Bot is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))