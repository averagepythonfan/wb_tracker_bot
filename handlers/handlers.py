__all__ = [
    'register_message_handlers'
]

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from sqdb import *
from sqlite3 import IntegrityError


help_str = ''' '''

async def help_command(message : types.Message):
    '''
    '''
    await message.reply(help_str)

#+
async def register_user_command(message : types.Message):
    '''Регистрирует пользователя в базе данных. По дефолту на бесплатном тарифе. Если пользователь уже зарегистрирован, сообщает ему об этом.
    '''
    try:
        await insert_user(message.from_user.id, message.from_user.username)
        await message.reply('Success')
    except IntegrityError:
        await message.reply('Already registred')



async def add_product_command(message : types.Message):
    '''
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
            await message.reply('Success')
        except ValueError:
            await message.reply('Введите валидный артикул')
    else:
        await message.reply('Превышен лимит')
    

async def my_products_command(message : types.Message):
    '''
    '''
    await message.reply('Products :')


def register_message_handlers(dp : Dispatcher):
    dp.register_message_handler(help_command, Command(commands=['help', 'помощь']))
    dp.register_message_handler(help_command, Text(['help', 'помощь']))
    dp.register_message_handler(register_user_command, Command(commands=['register', 'регистрация']))
    dp.register_message_handler(register_user_command, Text(['register', 'регистрация']))
    dp.register_message_handler(add_product_command, Command(commands=['add', 'add_product', 'wb', 'добавь', 'вб']))