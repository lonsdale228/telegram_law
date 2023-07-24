import os.path

from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from loader import dp


class GetFile(StatesGroup):
    get_file=State()

@dp.message(Text('📄Замінити файл'))
async def change_file(message:Message,state:FSMContext):
    await state.set_state(GetFile.get_file)
    await message.answer('Надішліть файл із корисною інформацією:')


async def get_extension(path:str):
    _, file_extension = os.path.splitext(path)
    return file_extension

@dp.message(GetFile.get_file)
async def get_file(message:Message,state:FSMContext):
    file = await state.bot.get_file(message.document.file_id)
    file_ext = await get_extension(file.file_path)

    if file_ext!='.pdf':
        await message.reply('Надішліть файл формату PDF!')
    else:
        #print(file.file_path)
        path=open(f'./files/info{file_ext}','wb')
        await state.clear()
        await state.bot.download_file(file.file_path,path)
        await message.reply('Файл замінено!')