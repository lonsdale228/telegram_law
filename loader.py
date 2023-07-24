from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN


storage = MemoryStorage()
bot = Bot(TOKEN,parse_mode="HTML")

dp = Dispatcher(storage=storage)


default_router = Router()
default_router.message.filter(F.chat.type == "private")
dp.include_router(default_router)

dp.message.filter(F.chat.type == "private")



# The awesome trottling middleware
# dp.callback_query.outer_middleware(ThrottlingMiddleware())
# dp.message.outer_middleware(ThrottlingMiddleware())