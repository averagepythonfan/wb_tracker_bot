__all__ = [
    'register_message_handlers'
]

import re
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from sqdb import transaction
from sqlite3 import IntegrityError
from time import localtime, strftime

# init exeption
class ZeroValues(BaseException):
    pass


# init inline keyboard
keyboard = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(
                text='Удалить',
                callback_data='delete_button_pressed')
keyboard.add(button_1)

kb_cancel = InlineKeyboardMarkup()
button_2 = InlineKeyboardButton(
                text='Отменить удаление',
                callback_data='cancel_button_pressed')
kb_cancel.add(button_2)


help_str = r'''Вас привествует бот Wildberries-Tracker.'
            'Зарегистрируйтесь (команда /register) и можете добавлять товары в трекер.'
            'Чтобы добавить товар в трекер отправьте команду "/add (артикул товара)" без скобочек и ковычек.'
            'При тарифе "free" у вас в доступе три трекера.'
            'Можно в любой момент удалять и добавлять другие товары для трекинга.'
            'Проверка цены происходит каждые 1-1,5 часа.'
            'Если товар поменяет свою цену, вам придет уведомление от бота.'''


# +
async def help_command(message: types.Message):
    '''Отправляет пользователю сообщение с описанием работы бота.'''
    await message.reply(help_str)

async def echo_command(message: types.Message):
    await message.reply(message)

# +
async def register_user_command(message: types.Message):
    '''Регистрирует пользователя в базе данных. По дефолту на бесплатном тарифе. Если пользователь уже зарегистрирован, сообщает ему об этом.
    '''
    try:
        async with transaction() as cur:
            cur.execute(
                f'''INSERT INTO users ( userid, username, status)
                        VALUES ( {message.from_user.id}, '{message.from_user.username}', 'free');'''
            )
        await message.reply('Успешно')
    except IntegrityError:
        await message.reply('Уже зарегистрированы')


# +
async def add_product_command(message: types.Message):
    '''Добавляет продукт в таблицу products. Максимальное количество 3 при тарифе "free".
    Не позволяет добавлять продукты не зарегистрированным пользователям. Так же не позволяет добавлять не валидные артикулы.
    '''
    
    async with transaction() as cur:
        lenght = cur.execute(
            f'''SELECT article FROM products
                WHERE userid = {message.from_user.id};'''
            ).fetchall()
    count = len(lenght)

    async with transaction() as cur:
        status = cur.execute(f'SELECT status FROM users WHERE userid = {message.from_user.id}').fetchall()
    
    if len(status) == 0:
        await message.reply('Зарегистрируйтесь')
    elif count < 3 or status == 'premium':
        try:
            async with transaction() as cur:
                cur.execute(
                    f'''INSERT INTO products VALUES ( {int(message.get_args())}, {message.from_user.id});'''
                )
            await message.reply('Успешно')
        except ValueError:
            await message.reply('Введите валидный артикул')
    else:
        await message.reply('Превышен лимит')

# +
async def delete_product_command(message: types.Message):
    '''Удаляет товар по артикулу. Если такого товара нет, сообщает об этом пользователю. Если товар успешно удален, также сообщает пользователю.
    '''
    try:   
        async with transaction() as cur:
            lenght = cur.execute(
                f'''SELECT article FROM products
                    WHERE article = {int(message.get_args())} AND userid = {message.from_user.id};'''
            ).fetchall()
        count = len(lenght)
        if count == 0:
            raise ZeroValues()
        
        async with transaction() as cur:
            cur.execute(f'DELETE FROM products WHERE article = {int(message.get_args())} AND userid = {message.from_user.id};')
        
        await message.reply('Товар успешно удален')
    except ValueError:
        await message.reply('Введите валидный артикул')
    except ZeroValues:
        await message.reply('Нет такого товара')
    

# +
async def my_products_command(message: types.Message):
    '''Возвращает список отслеживаемых товаров с ценами.
    '''
    async with transaction() as cur:
        articles = cur.execute(f'''
            SELECT article FROM products
            WHERE userid = {message.from_user.id};''').fetchall()
        
    for el in articles:
        async with transaction() as cur:
            name_and_price = cur.execute(f'''
                SELECT name, price, data FROM tracker
                WHERE article = {el[0]}
                ORDER BY data DESC
                LIMIT 1;''').fetchall()
        await message.answer(
            text=f'<b>Артикул</b>: {str(el[0])}\n'
                f'<b>Товар</b>: {name_and_price[0][0]}\n'
                f'<b>Цена</b>: {name_and_price[0][1]} <b>RUB</b>\n'
                f'''<b>Последнее обновление</b>: {strftime(
                    "%d.%m.%y, %H:%M MCK",
                    localtime(name_and_price[0][2]))}''',
                parse_mode='HTML',
                reply_markup=keyboard
        )

# +
async def callback_delete(callback: CallbackQuery):
    '''Удаляет выбранный товар из базы данных products
    '''
    text = callback.message.text
    article = int(text[9:text.find('Товар')-1])
    userid = int(callback.from_user.id)
    async with transaction() as cur:
        cur.execute(
            f'''DELETE FROM products
            WHERE article = {article} AND userid = {userid};''')
    await callback.message.delete()
    await callback.message.answer(
        text=f'Товар с артикулом {article} успешно удален',
        reply_markup=kb_cancel
    )
    await callback.answer()


async def callback_cancel(callback: CallbackQuery):
    '''Отменяет удаление'''
    text =  callback.message.text
    article = int(text[17:text.find('успешно')-1])
    userid = int(callback.from_user.id)
    async with transaction() as cur:
        cur.execute(
            f'''INSERT INTO products
                VALUES ( {article}, {userid});'''
        )
    await callback.message.delete()
    await callback.message.answer(f'Товар с артикулом {article} возвращен в трекер.')
    await callback.answer()

def register_message_handlers(dp : Dispatcher):
    dp.register_message_handler(echo_command,
                                Text(['echo']))
    dp.register_message_handler(help_command,
                                Command(commands=['help', 'помощь']))
    dp.register_message_handler(help_command,
                                Text(['help', 'помощь']))
    dp.register_message_handler(register_user_command,
                                Command(commands=['register', 'регистрация']))
    dp.register_message_handler(register_user_command,
                                Text(['register', 'регистрация']))
    dp.register_message_handler(add_product_command,
                                Command(commands=['add', 'add_product', 'wb', 'добавь', 'вб']))
    dp.register_message_handler(my_products_command,
                                Command(commands=['my_products', 'продукты']))
    dp.register_message_handler(my_products_command,
                                Text(['my_products', 'продукты']))
    dp.register_message_handler(delete_product_command,
                                Command(commands=['delete', 'удалить']))
    dp.register_callback_query_handler(callback_delete, 
                                       text='delete_button_pressed')
    dp.register_callback_query_handler(callback_cancel, 
                                       text='cancel_button_pressed')