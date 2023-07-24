from aiogram import types, F
from aiogram.enums import ParseMode
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from db.add_phone_number import add_phone
from db.add_treatment import add_treatment
from filters.isUser import IsUser
from keyboards.dict_to_keyboard import get_keyboard
from keyboards.inline_menu import menu, admin_service
from loader import dp, bot
from strings.strings import start_text, choose_consult_text, accept_menu_text, text_consult_desc, phone_consult_desc, \
    office_consult_desc


async def get_name(menu_name,btn):
    # print("test: ", menu_name,btn)
    try:
        btn_name=menu[menu_name][btn]
    except KeyError:
        btn_name='Інше питання 🧑‍⚖️ АВ ОВ'
    return btn_name





#return to consult choise
@dp.callback_query(IsUser(),Text('consult_return'))
async def sedasdand_random_value(callback: types.CallbackQuery,state:FSMContext):
    data=await state.get_data()
    service_type=data["service_type"]

    await callback.message.edit_text(f'{choose_consult_text%(await get_name("services",service_type))}',reply_markup=await get_keyboard('cons_type'))

#return to service choise
@dp.callback_query(IsUser(),Text('service_return'))
async def sedasdand_random_value(callback: types.CallbackQuery,state:FSMContext):
    #await state.clear()
    await callback.message.edit_text(
        "З якого питання Вас цікавить консультація?",
        reply_markup=await get_keyboard('services'),
        parse_mode=ParseMode.HTML
    )

@dp.callback_query(IsUser(),F.data.contains('service'))
async def send_random_value(callback: types.CallbackQuery,state:FSMContext):
    data=await state.get_data()

    #print(data)


    if data['service_type']=='':
        await state.update_data(service_type=callback.data)


    name_of_service=await get_name('services',callback.data)
    await callback.message.edit_text(f'{choose_consult_text%(name_of_service)}',reply_markup=await get_keyboard('cons_type'))

@dp.callback_query(IsUser(),Text('phone_back'))
@dp.callback_query(IsUser(),F.data.contains('consult'))
async def show_consult(callback:types.CallbackQuery,state:FSMContext):
    data = await state.get_data()

    await state.update_data(phone_number='')

    if "back" not in callback.data:
        await state.update_data(consult_type=callback.data)
        consult_name = menu['cons_type'][callback.data]
        consult = callback.data
    else:
        consult_name = menu['cons_type'][data['consult_type']]
        consult = data['consult_type']


    service_type=data['service_type']
    # print("Aboba: ", service_type)

    # service_name=await get_name('services',service_type)
    # consult_name=await get_name('cons_type',callback.data)

    service_name = menu['services'][service_type]


    consult_description=""
    # print(consult)
    match consult:
        case "consult_text":
            consult_description=text_consult_desc
        case "consult_phone":
            consult_description=phone_consult_desc
        case "consult_office":
            consult_description=office_consult_desc

    #print("cons_desc: ", consult_description)

    await callback.message.edit_text(f'{accept_menu_text%(service_name,consult_name)} \n{consult_description}',reply_markup=await get_keyboard('accept'))




class Form(StatesGroup):
    get_phone_number=State()
    phone_number_approve=State()

#finish menu
@dp.callback_query(IsUser(),Text('phone_edit'))
@dp.callback_query(IsUser(),Text('accept'))
async def send_accept_message(callback:types.CallbackQuery,state:FSMContext):
    data = await state.get_data()
    service_type = data['service_type']
    consult_type = data['consult_type']

    # print("service_type: ",service_type)

    try:
        custom_question=data['custom_question']
        phone_number=data['phone_number']
    except KeyError:
        custom_question=''
        phone_number=''
    #(consult_type == 'consult_phone' or consult_type == 'another') and
    if  phone_number=='':
        await state.set_state(Form.get_phone_number)
        await callback.message.edit_text("Введіть Ваш номер для зв'язку:")
    else:
        await add_treatment(callback.from_user.id,service_type,consult_type,custom_text=custom_question)

        # await add_phone(callback.from_user.id,phone_number)
        await state.clear()
        await callback.message.edit_text("Ми незабаром з Вами зв'яжемося!")




def phone_check(input_string,length=20):
    import re
    pattern = r"^[0-9+\-—–()]+$"
    return bool(re.match(pattern, input_string) and len(input_string)<length)


@dp.callback_query(IsUser(),Text('check_return'))
async def save_number(call:types.CallbackQuery,state:FSMContext):
    data=await state.get_data()
    await state.update_data(custom_text='')
    phone_number=data["phone_number"]

    buttons = [
        [types.InlineKeyboardButton(text="✅Підтвердити номер", callback_data="phone_accept")],
        [types.InlineKeyboardButton(text="✍️Відредагувати", callback_data="phone_edit")],
        [types.InlineKeyboardButton(text="🔙Повернутися", callback_data="phone_back")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)

    await call.message.edit_text(f"Ваш номер телефону: \n\n{phone_number}", reply_markup=keyboard)


@dp.message(IsUser(),Form.get_phone_number)
async def save_number(message:Message,state:FSMContext):
    if phone_check((message.text).strip()):
        await state.update_data(phone_number=message.text)
        await state.set_state(Form.phone_number_approve)

        buttons = [
            [types.InlineKeyboardButton(text="✅Підтвердити номер", callback_data="phone_accept")],
            [types.InlineKeyboardButton(text="✍️Відредагувати", callback_data="phone_edit")],
            [types.InlineKeyboardButton(text="🔙Повернутися", callback_data="phone_back")]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)

        await message.reply(f"Ваш номер телефону: \n\n{message.text}", reply_markup=keyboard)

    else:
        await message.reply("""Ви ввели неприпустимий номер телефону!\n\n "Введіть Ваш номер для зв'язку:""")
        await state.set_state(Form.get_phone_number)



@dp.callback_query(IsUser(),Text('agree'))
# @dp.callback_query(IsUser(),Text('phone_accept'))
async def phone_consult_approve(call:types.CallbackQuery,state:FSMContext):
    data=await state.get_data()
    phone_number=data['phone_number']
    service_type=data['service_type']
    service_name=menu['services'][service_type]
    consult_type=data['consult_type']

    try:
        custom_question=data['custom_question']
    except KeyError:
        custom_question=''


    await add_treatment(call.from_user.id, service_type, consult_type, custom_text=custom_question)
    await add_phone(call.from_user.id,phone_number)
    await state.clear()
    await call.message.edit_text("Ми незабаром з Вами зв'яжемося!!!!")

    send_service=admin_service[service_type]

    for admin in send_service:
        await bot.send_message(chat_id=admin,text=f'<b>Новий запит на консультацію!</b>\n\n'
                                                  f'Від: {call.from_user.full_name[:30]}\n'
                                                  f'Телеграм клієнта: <a href="tg://user?id={call.from_user.id}">Клік</a>\n'
                                                  f'Номер телефону: <code>{phone_number}</code>\n'
                                                  f'Напрям: {service_name}\n'
                                                  f'Тип консультації: {menu["cons_type"][consult_type]} \n'
                                                  f'Ситуація: \n'
                                                  f'"{custom_question}"',parse_mode=ParseMode.HTML)


