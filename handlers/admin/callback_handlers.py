import asyncio

import aiogram
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db.change_user_activity import change_activity
from db.get_user import get_all_users
from filters.isAdmin import IsAdmin
from handlers.admin.menu_handlers import GetMessage
from loader import dp, bot


async def send_message_to_users(users, text_message):
    for user in users:
        try:
            await bot.send_message(chat_id=user[0], text=text_message,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
        except aiogram.exceptions.TelegramForbiddenError:
            await change_activity(user[0],is_active=0)
        await asyncio.sleep(0.2)

@dp.callback_query(IsAdmin(),Text('mailing_accept'))
async def start_mailing(call:CallbackQuery,state:FSMContext):
    data=await state.get_data()
    text_message=data['mailing_text']

    users=await get_all_users()

    await call.message.edit_text('Розсилка розпочата!')
    await send_message_to_users(users,text_message)



@dp.callback_query(IsAdmin(),Text('mailing_edit'))
async def mailing(call:CallbackQuery,state:FSMContext):
    await state.set_state(GetMessage.get_text)

    await call.message.edit_text("Введіть повідомлення, яке б Ви хотіли надіслати клієнтам:")


@dp.callback_query(IsAdmin(),Text('mailing_back'))
async def admin_back_menu(call:CallbackQuery,state:FSMContext):
    await state.clear()
    buttons = [
        [types.KeyboardButton(text='Виконати розсилку'),types.KeyboardButton(text='Експортувати базу даних'),types.KeyboardButton(text='📄Замінити файл')]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer("Ви авторизовані як адмін! Оберіть команди які необхідно виконати, або чекайте на заяви)",reply_markup=keyboard)