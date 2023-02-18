from aiogram import Bot, Dispatcher, executor
from config import TOKEN
from handlers import register_message_handlers, commands_for_bot


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


async def on_startup(_):
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
