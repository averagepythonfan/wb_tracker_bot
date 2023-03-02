from aiogram import Bot, Dispatcher, executor
from config import TOKEN
from handlers import register_message_handlers, commands_for_bot
from sqdb import transaction
from sqlalchemy import text
from logger import logger


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


# initial queries, registering message handlers and menu commands setup
async def on_startup(_):
    async with transaction() as cur:
        cur.execute(text('''
            CREATE TABLE IF NOT EXISTS users
            (userid INTEGER NOT NULL PRIMARY KEY,
            status TEXT NOT NULL );'''))

    async with transaction() as cur:
        cur.execute(text('''
            CREATE TABLE IF NOT EXISTS products
            (article INTEGER NOT NULL,
            userid INTEGER NOT NULL);'''))

    async with transaction() as cur:
        cur.execute(text('''
            CREATE TABLE IF NOT EXISTS tracker
            (article INTEGER NOT NULL,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            userid INTEGER NOT NULL,
            data INTEGER NOT NULL);'''))
    register_message_handlers(dp=dp)
    await bot.set_my_commands(commands=commands_for_bot)
    logger.info('Bot started!')


if __name__ == '__main__':
    try:
        executor.start_polling(dispatcher=dp,
                               on_startup=on_startup,
                               skip_updates=True)
    except KeyboardInterrupt:
        logger.critical('Bot closed. Goodbye!')
