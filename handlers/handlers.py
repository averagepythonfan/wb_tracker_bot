__all__ = [
    'register_message_handlers'
]

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from sqdb import *
from sqlite3 import IntegrityError


class ZeroValues(BaseException):
    pass


help_str = '''Вас привествует бот Wildberries-Tracker. Зарегистрируйтесь (команда /register) и можете добавлять товары в трекер.

Чтобы добавить товар в трекер отправьте команду "/add (артикул товара)" без скобочек и ковычек.

При тарифе "free" у вас в доступе три трекера. Можно в любой момент удалять и добавлять другие товары для трекинга.

Проверка цены происходит каждые 1-1,5 часа. Если товар поменяет свою цену, вам придет уведомление от бота.'''


#+
async def help_command(message : types.Message):
    '''Отправляет пользователю сообщение с описанием работы бота.'''
    await message.reply(help_str)

#+
async def register_user_command(message : types.Message):
    '''Регистрирует пользователя в базе данных. По дефолту на бесплатном тарифе. Если пользователь уже зарегистрирован, сообщает ему об этом.
    '''
    try:
        await insert_user(message.from_user.id, message.from_user.username)
        await message.reply('Успешно')
    except IntegrityError:
        await message.reply('Уже зарегистрированы')


#+
async def add_product_command(message : types.Message):
    '''Добавляет продукт в таблицу products. Максимальное количество 3 при тарифе "free".
    Не позволяет добавлять продукты не зарегистрированным пользователям. Так же не позволяет добавлять не валидные артикулы.
    '''
    count = await check_products_count(message.from_user.id)
    status = await check_status(message.from_user.id)
    if len(status) == 0:
        await message.reply('Зарегистрируйтесь')
    elif count < 3 or status == 'premium':
        try:
            await insert_product(
                int(message.get_args()),
                message.from_user.id
            )
            await message.reply('Успешно')
        except ValueError:
            await message.reply('Введите валидный артикул')
    else:
        await message.reply('Превышен лимит')

#+
async def delete_product_command(message : types.Message):
    '''Удаляет товар по артикулу. Если такого товара нет, сообщает об этом пользователю. Если товар успешно удален, также сообщает пользователю.
    '''
    try:
        count = await check_product_exist(int(message.get_args()), message.from_user.id)
        if count == 0:
            raise ZeroValues()
        await delete_product(int(message.get_args()), message.from_user.id)
        await message.reply('Товар успешно удален')
    except ValueError:
        await message.reply('Введите валидный артикул')
    except ZeroValues:
        await message.reply('Нет такого товара')
    

async def my_products_command(message : types.Message):
    '''
    '''
    for el in fetch_products(message.from_user.id):
        pass


def register_message_handlers(dp : Dispatcher):
    dp.register_message_handler(help_command, Command(commands=['help', 'помощь']))
    dp.register_message_handler(help_command, Text(['help', 'помощь']))
    dp.register_message_handler(register_user_command, Command(commands=['register', 'регистрация']))
    dp.register_message_handler(register_user_command, Text(['register', 'регистрация']))
    dp.register_message_handler(add_product_command, Command(commands=['add', 'add_product', 'wb', 'добавь', 'вб']))
    dp.register_message_handler(my_products_command, Command(commands=['my_products', 'продукты']))
    dp.register_message_handler(my_products_command, Text(['my_products', 'продукты']))
    dp.register_message_handler(delete_product_command, Command(commands=['delete', 'удалить']))