import datetime
import os

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile


from filters.isAdmin import IsAdmin
from loader import dp


class GetMessage(StatesGroup):
    get_text=State()


@dp.message(IsAdmin(),Text('Експортувати базу даних'))
async def export_database(message:Message,state:FSMContext):
    await state.set_state(None)
    file = os.path.abspath('tg.db')
    file = FSInputFile(file)
    await message.answer_document(file,caption="База даних: ")

@dp.message(IsAdmin(),Text('Виконати розсилку'))
async def mailing_edit(message:Message,state:FSMContext):
    await state.set_state(GetMessage.get_text)

    await message.answer("Введіть повідомлення, яке б Ви хотіли надіслати клієнтам:")


@dp.message(IsAdmin(),GetMessage.get_text)
async def get_text(message:Message,state:FSMContext):
    if len(message.text)>3000:
        await message.answer(f'Ви ввели занадто довге повідомлення! Відредагуйте будь ласка.')
    else:
        buttons=[
            [types.InlineKeyboardButton(text="✅Підтвердити розсилку", callback_data="mailing_accept")],
            [types.InlineKeyboardButton(text="✍️Відредагувати", callback_data="mailing_edit")],
            [types.InlineKeyboardButton(text="🔙Повернутися", callback_data="mailing_back")]
                  ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)

        await state.update_data(mailing_text=message.html_text)

        await message.answer(f"Підтвердіть надсилання, або відредагуйте текст: \n\n{message.html_text}",reply_markup=keyboard,parse_mode=ParseMode.HTML)




@dp.message(IsAdmin(),Text('Статистика'))
async def send_stat(message:Message):
    from db.get_stat import get_click_stat,get_treatments_from_day,get_new_users
    btns_get_info=[
        '📞Наші контакти📞',
        '✍️Записатися на консультацію✍️',
        '📝Корисна інформація📝',
        'Підтвердити контакти'
    ]

    days = [1, 7, 30, 0]

    # text='Кліків: \n'
    # for btn in btns_get_info:
    #     clicks=await get_clicks(btn_name=btn)
    #     text=text+f"{btn}: \n"\
    #               f"Сьогодні: {clicks['day']} \n"\
    #               f"Тиждень: {clicks['week']}\n"\
    #               f"Місяць: {clicks['month']}\n"\
    #               f"Увесь час: {clicks['all_time']}\n\n"

    text = 'Кліків: \n'
    for btn in btns_get_info:

        clicks=[await get_click_stat(btn,day) for day in days]
        text=text+f"{btn}: \n"\
                  f"24 години: {clicks[0]} \n"\
                  f"Тиждень: {clicks[1]}\n"\
                  f"Місяць: {clicks[2]}\n"\
                  f"Увесь час: {clicks[3]}\n\n"


    treatments=[await get_treatments_from_day(day) for day in days]
    text=text+f"Консультацій:\n" \
              f"24 години: {treatments[0]} \n"\
              f"Тиждень: {treatments[1]}\n"\
              f"Місяць: {treatments[2]}\n"\
              f"Увесь час: {treatments[3]}\n\n"


    new_users=[await get_new_users(day) for day in days]
    text=text+f"Нових користувачів:\n" \
              f"24 години: {new_users[0]} \n"\
              f"Тиждень: {new_users[1]}\n"\
              f"Місяць: {new_users[2]}\n"\
              f"Увесь час: {new_users[3]}\n\n"


    await message.answer(text=text)