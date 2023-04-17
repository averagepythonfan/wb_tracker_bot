import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_message_handlers
from config import DATABASE, HOST, TOKEN, USERNAME, PASSWORD
from db import BaseModel, get_session_maker, proceed_schemas, create_async_engine
from sqlalchemy.engine import URL



async def main():
    '''Main command which set logging and polling'''

    logging.basicConfig(level=logging.DEBUG)

    dp = Dispatcher()
    bot = Bot(token=TOKEN)

    register_message_handlers(dp)

    postgres_url = URL.create(
        drivername='postgresql+asyncpg',
        username=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=5433,
        database=DATABASE
    )

    async_engine = create_async_engine(url=postgres_url)
    session_maker = get_session_maker(async_engine)
    # await proceed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('goodbye!')
