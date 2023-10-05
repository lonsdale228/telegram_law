from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

from filters.isAdmin import IsAdmin
from loader import dp


@dp.message(IsAdmin(),Command("start"))
async def admin_start(message:Message):
    buttons = [
        [types.KeyboardButton(text='Виконати розсилку'),types.KeyboardButton(text='Експортувати базу даних')],
         [types.KeyboardButton(text='📄Замінити файл'),types.KeyboardButton(text='Статистика')]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Ви авторизовані як адмін! Оберіть команди які необхідно виконати, або чекайте на заяви)",reply_markup=keyboard)