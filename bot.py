from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import cur, conn

def get_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(" Бесплатная генерация", callback_data="free"),
        InlineKeyboardButton(" 3 генерации — 200 ₽", callback_data="p3"),
        InlineKeyboardButton(" 5 генераций — 300 ₽", callback_data="p5"),
        InlineKeyboardButton(" 10 генераций — 760 ₽", callback_data="p10"),
        InlineKeyboardButton(" 100 генераций — 1699 ₽", callback_data="p100")
    )
    return kb

def register(dp: Dispatcher):

    @dp.message_handler(commands=["start"])
    async def start(msg: types.Message):
        cur.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (msg.from_user.id,))
        conn.commit()
        await msg.answer(
            " AI Генерация изображений\n\n"
            "1 бесплатная генерация\n"
            "Платные пакеты ниже ",
            reply_markup=get_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "free")
    async def free(call: types.CallbackQuery):
        cur.execute("SELECT free_used FROM users WHERE user_id=?", (call.from_user.id,))
        used = cur.fetchone()[0]
        if used:
            await call.answer(" Бесплатная генерация уже использована", show_alert=True)
            return
        cur.execute("UPDATE users SET free_used=1 WHERE user_id=?", (call.from_user.id,))
        conn.commit()
        await call.message.answer(" Бесплатная генерация выполнена (заглушка)")
        await call.answer()

    @dp.callback_query_handler(lambda c: c.data.startswith("p"))
    async def pay(call: types.CallbackQuery):
        prices = {
            "p3": "200 ₽ / 3 генерации",
            "p5": "300 ₽ / 5 генераций",
            "p10": "760 ₽ / 10 генераций",
            "p100": "1699 ₽ / 100 генераций"
        }
        await call.message.answer(
            f" Оплата пакета: {prices[call.data]}\n\n"
            "После оплаты нажмите «Я оплатил»",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(" Я оплатил", callback_data="paid")
            )
        )
        await call.answer()

    @dp.callback_query_handler(lambda c: c.data == "paid")
    async def paid(call: types.CallbackQuery):
        await call.message.answer(
            " Платёж в обработке\n"
            "(Для модерации YooKassa — заглушка)"
        )
        await call.answer()