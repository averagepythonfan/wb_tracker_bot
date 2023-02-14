import logging
from aiogram import Bot, Dispatcher, executor
from config import TOKEN
from sqdb import connect_to_db
from handlers import register_message_handlers


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

register_message_handlers(dp=dp)

async def on_startup(_):
    connect_to_db()
    print('Connect to db')

if __name__ == '__main__':
    try:
        executor.start_polling(dispatcher=dp, on_startup=on_startup)
    except KeyboardInterrupt:
        print('Goodbye!')