import asyncio


from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db.get_user import get_all_users
from filters.isAdmin import IsAdmin
from handlers.admin.menu_handlers import GetMessage
from loader import dp, bot


async def send_message_to_users(users, text_message):
    tasks = [asyncio.create_task(bot.send_message(chat_id=user[0], text=text_message)) for user in users]
    await asyncio.gather(*tasks)


@dp.callback_query(IsAdmin(),Text('mailing_accept'))
async def start_mailing(call:CallbackQuery,state:FSMContext):
    data=await state.get_data()
    text_message=data['mailing_text']

    users=await get_all_users()

    await send_message_to_users(users,text_message)

    # for admin_id in ADMINS:
    #     print(admin_id)
    #     await bot.send_message(chat_id=admin_id,text=text_message)
    await call.message.edit_text('Розсилка розпочата!')

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