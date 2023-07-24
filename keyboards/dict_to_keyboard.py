from aiogram import types

from keyboards.inline_menu import menu


async def get_keyboard(menu_name:str)->types.InlineKeyboardMarkup:

    l=[i for i in menu[menu_name].keys()]
    buttons=[]
    for btn in l:
        buttons.append([types.InlineKeyboardButton(text=menu[menu_name][btn], callback_data=f"{btn}")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# async def get_reply_keyboard(menu_name:str)->types.ReplyKeyboardMarkup:
#     l = [i for i in reply_menu[menu_name].keys()]
#     buttons = []
#     for btn in l:
#         buttons.append([types.KeyboardButton(text=reply_menu[menu_name][btn])])
#     #print(buttons)
#     keyboard = types.ReplyKeyboardMarkup(keyboard=buttons)
#     return keyboard