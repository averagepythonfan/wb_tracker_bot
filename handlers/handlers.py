__all__ = [
    'register_message_handlers'
]

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from ..sqdb import insert_user

help_str = ''' '''

async def help_command(message : types.Message):
    '''
    '''
    await message.reply(help_str)

async def register_user_command(message : types.Message):
    '''
    '''
    await insert_user(message.from_user.id, message.from_user.username)
    await message.reply('Success')

async def add_product_command(message : types.Message):
    '''
    '''
    await message.reply('Success')

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
    dp.register_message_handler(add_product_command, Text(['add', 'add_product', 'wb', 'добавь', 'вб']))