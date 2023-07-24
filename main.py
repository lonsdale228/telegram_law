import asyncio

import middlewares
from db.run import db_start
from loader import dp, bot
import logging

import handlers

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    middlewares.setup(dp)
    asyncio.run(db_start())
    asyncio.run(main())