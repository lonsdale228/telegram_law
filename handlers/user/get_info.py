from aiogram import F, types
from aiogram.enums import ParseMode
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, Message

from config import admin_service
from db.add_phone_number import add_phone
from db.add_stat import add_click
from db.add_treatment import add_treatment
from filters.isUser import IsUser
from keyboards.dict_to_keyboard import get_keyboard
from keyboards.inline_menu import menu
from loader import dp, bot
from strings.strings import choose_consult_text


class Form(StatesGroup):
    custom_question=State()

@dp.callback_query(IsUser(),Text('phone_accept'))
#@dp.callback_query(IsUser(),F.data.contains('another'))
async def get_more_info(callback: types.CallbackQuery,state:FSMContext):
    await state.set_state(Form.custom_question)

    await add_click(btn_name="Підтвердити контакти")

    buttons = [
        [types.InlineKeyboardButton(text="🔙Повернутися", callback_data="text_back")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)


    msg=await callback.message.edit_text('Опишіть Вашу проблему: ',reply_markup=keyboard)

    await state.update_data(declare_problem=msg.message_id)




# @dp.message(IsUser(),Form.custom_question)
# async def process_question(message:Message,state:FSMContext):
#     await state.update_data(custom_question=message.text)
#     #await state.update_data(service_type='another')
#
#     #print(message.text)
#     await message.answer(f'Ваше питання:\n\n"{message.text}"',reply_markup=await get_keyboard('check_question'))

@dp.message(IsUser(),Form.custom_question)
async def get_custom_question(message:Message,state:FSMContext):


    data = await state.get_data()
    phone_number = data['phone_number']
    service_type = data['service_type']
    service_name = menu['services'][service_type]
    consult_type = data['consult_type']

    try:
        edit_msg=data['declare_problem']
        await bot.delete_message(chat_id=message.from_user.id,message_id=edit_msg)
    except KeyError:
        ...


    custom_question = message.text

    await add_treatment(message.from_user.id, service_type, consult_type, custom_text=custom_question)

    await state.clear()


    await message.answer("Дякуємо! Адвокат зв'яжеться з Вами протягом 10 хв.\n"
                                 "<em>*час очікування може збільшитися якщо конкретний адвокат зараз у суді або запит залишено в неробочій період.</em>")

    send_service = admin_service[service_type]

    for admin in send_service:
        await bot.send_message(chat_id=admin, text=f'<b>Новий запит на консультацію!</b>\n\n'
                                                   f'Від: {message.from_user.full_name[:30]}\n'
                                                   f'Телеграм клієнта: <a href="tg://user?id={message.from_user.id}">Клік</a>\n'
                                                   f'Контакти: <code>{phone_number}</code>\n'
                                                   f'Напрям: {service_name}\n'
                                                   f'Тип консультації: {menu["cons_type"][consult_type]} \n'
                                                   f'Ситуація: \n\n'
                                                   f'"{custom_question}"', parse_mode=ParseMode.HTML)

@dp.callback_query(IsUser(),Text('change_text'))
async def change_question(callback: types.CallbackQuery,state:FSMContext):
    await state.set_state(Form.custom_question)
    await callback.message.edit_text('Введіть Ваше питання: ')


