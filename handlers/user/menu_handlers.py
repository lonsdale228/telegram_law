#main_menu
import os

from aiogram import F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from db.add_user import add_user
from db.get_user import get_user
from filters.isUser import IsUser
from keyboards.dict_to_keyboard import get_keyboard
from loader import dp, bot
from strings.strings import our_contacts


@dp.message(IsUser(),F.text.contains('Записатися на консультацію'))
async def asdasddsa(message:Message,state:FSMContext):
    await state.update_data(service_type='')

    test = await get_user(message.from_user.id)
    if not test:
        await add_user(message.from_user.id, message.from_user.full_name)

    markup=await get_keyboard('services')
    await message.answer('З якого питання Вас цікавить консультація?',reply_markup=markup)

@dp.message(IsUser(),F.text.contains('Наші контакти'))
async def asdasddsa(message:Message):
    await message.answer(our_contacts,
        parse_mode=ParseMode.HTML,disable_web_page_preview=True)

@dp.message(IsUser(),F.text.contains('Корисна інформація'))
async def send_more_info(message:Message):
    file=os.path.abspath('files/file.pdf')
    file = FSInputFile(file)
    await bot.send_document(message.from_user.id,file,caption='Детальнішу інформацію можливо отримати тут')