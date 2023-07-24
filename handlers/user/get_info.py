from aiogram import F, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, Message

from filters.isUser import IsUser
from keyboards.dict_to_keyboard import get_keyboard
from loader import dp
from strings.strings import choose_consult_text


class Form(StatesGroup):
    custom_question=State()

@dp.callback_query(IsUser(),Text('phone_accept'))
#@dp.callback_query(IsUser(),F.data.contains('another'))
async def get_more_info(callback: types.CallbackQuery,state:FSMContext):
    await state.set_state(Form.custom_question)
    await callback.message.edit_text('Опишіть Вашу проблему: ')




@dp.message(IsUser(),Form.custom_question)
async def process_question(message:Message,state:FSMContext):
    await state.update_data(custom_question=message.text)
    #await state.update_data(service_type='another')

    #print(message.text)
    await message.answer(f'Ваше питання:\n\n"{message.text}"',reply_markup=await get_keyboard('check_question'))



@dp.callback_query(IsUser(),Text('change_text'))
async def change_question(callback: types.CallbackQuery,state:FSMContext):
    await state.set_state(Form.custom_question)
    await callback.message.edit_text('Введіть Ваше питання: ')


