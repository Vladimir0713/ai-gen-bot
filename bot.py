import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Переменные окружения
API_TOKEN = os.getenv("BOT_TOKEN")
YOOKASSA_TOKEN = os.getenv("YOOKASSA_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Кнопка оплаты
pay_kb = InlineKeyboardMarkup(row_width=1)
pay_kb.add(InlineKeyboardButton("Я оплатил", callback_data="paid"))

# Бесплатная пробная генерация
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! У тебя есть 1 бесплатная генерация.\n"
        "Для покупки пакетов используй /buy",
        reply_markup=None
    )

# Список пакетов
packages = {
    "3 генерации": 200,
    "5 генераций": 300,
    "10 генераций": 760,
    "100 генераций": 1699
}

@dp.message(Command("buy"))
async def cmd_buy(message: types.Message):
    text = "Выбери пакет генераций:\n"
    for name, price in packages.items():
        text += f"{name} — {price} ₽\n"
    await message.answer(text, reply_markup=pay_kb)

# Обработчик нажатия "Я оплатил"
@dp.callback_query(lambda c: c.data == "paid")
async def payment_confirm(call: types.CallbackQuery):
    await call.message.answer("Оплата подтверждена! Ты можешь использовать генерации.")

# Заглушка для генерации AI
@dp.message(F.text)
async def generate_ai(message: types.Message):
    # TODO: подключить реальный AI генератор
    await message.answer(f"Генерирую изображение по запросу: {message.text}\n(Заглушка)")
