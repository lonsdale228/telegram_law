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


@dp.message(Text('Експортувати базу даних'))
async def export_database(message:Message):
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

        await state.update_data(mailing_text=message.text)

        await message.answer(f"Підтвердіть надсилання, або відредагуйте текст: \n\n{message.text}",reply_markup=keyboard,parse_mode=ParseMode.HTML)





