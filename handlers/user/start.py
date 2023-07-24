from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db.add_user import add_user
from db.get_user import get_user
from filters.isUser import IsUser
from loader import dp, bot
from strings.strings import start_text

async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/start", description="Запуск боту")
    ]
    await bot.set_my_commands(bot_commands)

@dp.message(IsUser(),Command("start"))
async def start_message(message: types.Message,state:FSMContext):

    #print(test,type(test))



    await setup_bot_commands()


    await state.clear()
    await state.update_data(service_type='')
    test = await get_user(message.from_user.id)
    if not test:
        await add_user(message.from_user.id,message.from_user.full_name)


    buttons=[
        [types.KeyboardButton(text='✍️Записатися на консультацію✍️')],
        [types.KeyboardButton(text='📝Корисна інформація📝'),types.KeyboardButton(text='📞Наші контакти📞')]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons,resize_keyboard=True)

    await message.answer(
        start_text,
        reply_markup= keyboard,
        parse_mode=ParseMode.HTML
    )


#+'<a href="tg://user?id=317465871">user</a>'