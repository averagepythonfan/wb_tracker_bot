from aiogram import Bot, Dispatcher, executor
from config import TOKEN, DATABASE
from handlers import register_message_handlers, commands_for_bot
from sqdb import transaction


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


# initial queries, registering message handlers and menu commands setup
async def on_startup(_):
    async with transaction(db_name=DATABASE) as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users
            (userid INTEGER NOT NULL,
            username TEXT NOT NULL PRIMARY KEY,
            status TEXT NOT NULL;''')

    async with transaction(db_name=DATABASE) as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS products
            (article INTEGER NOT NULL,
            userid INTEGER NOT NULL);''')

    async with transaction(db_name=DATABASE) as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tracker
            (article INTEGER NOT NULL,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            userid INTEGER NOT NULL,
            data INTEGER NOT NULL);''')
    register_message_handlers(dp=dp)
    await bot.set_my_commands(commands=commands_for_bot)
    print('Start!')


if __name__ == '__main__':
    try:
        executor.start_polling(dispatcher=dp,
                               on_startup=on_startup,
                               skip_updates=True)
    except KeyboardInterrupt:
        print('Goodbye!')
