__all__ = [
    'register_message_handlers'
]
from config import ADMIN_ID
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from sqdb import transaction
from sqlite3 import IntegrityError
from time import localtime, strftime
from .inlinekb import kb_delete, kb_register, kb_cancel_prem
from .callbacks import *

# init exeption
class ZeroValues(BaseException):
    pass



help_str = '''Вас привествует бот Wildberries-Tracker.\n
Зарегистрируйтесь (команда /register) и можете добавлять товары в трекер.\n
Чтобы добавить товар в трекер отправьте команду "/add (артикул товара)" без скобочек и ковычек.\n
При тарифе "free" у вас в доступе три трекера.\n
Можно в любой момент удалять и добавлять другие товары для трекинга.\n
Проверка цены происходит каждые 1-1,5 часа.\n
Если товар поменяет свою цену, вам придет уведомление от бота.'''


# +
async def help_command(message: types.Message):
    '''Отправляет пользователю сообщение с описанием работы бота.'''
    await message.reply(help_str, reply_markup=kb_register)

async def echo_command(message: types.Message):
    await message.reply(message)

# +
async def register_user_command(message: types.Message):
    '''Регистрирует пользователя в базе данных. По дефолту на бесплатном тарифе. Если пользователь уже зарегистрирован, сообщает ему об этом.
    '''
    try:
        async with transaction() as cur:
            cur.execute(f'''
                INSERT INTO users ( userid, username, status)
                VALUES ( {message.from_user.id}, '{message.from_user.username}', 'free');''')
        await message.reply('Успешно')
    except IntegrityError:
        await message.reply('Уже зарегистрированы')


async def add_product_command(message: types.Message):
    '''Добавляет продукт в таблицу products. Максимальное количество 3 при тарифе "free".
    Не позволяет добавлять продукты не зарегистрированным пользователям. Так же не позволяет добавлять не валидные артикулы.
    '''
    
    async with transaction() as cur:
        lenght = cur.execute(f'''
            SELECT article FROM products
            WHERE userid = {message.from_user.id};'''
        ).fetchall()
    count = len(lenght)

    async with transaction() as cur:
        status = cur.execute(f'''
            SELECT status FROM users WHERE userid = {message.from_user.id};''').fetchall()
    
    if len(status) == 0:
        await message.reply('Зарегистрируйтесь')
    elif count < 3 or status[0][0] == 'premium':
        try:
            async with transaction() as cur:
                cur.execute(f'''
                    INSERT INTO products VALUES ( {int(message.get_args())}, {message.from_user.id});'''
                )
            await message.reply('Успешно')
        except ValueError:
            await message.reply('Введите валидный артикул')
    else:
        await message.reply('Превышен лимит')


async def delete_product_command(message: types.Message):
    '''Удаляет товар по артикулу. Если такого товара нет, сообщает об этом пользователю. Если товар успешно удален, также сообщает пользователю.
    '''
    try:   
        async with transaction() as cur:
            lenght = cur.execute(f'''
                SELECT article FROM products
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
        try:
            int(name_and_price[0][1])
        except IndexError:
            await message.answer(f'Артикул {el[0]} пока не имеет обновлении!')
            continue
        await message.answer(
            text=f'<b>Артикул</b>: {str(el[0])}\n'
                f'<b>Товар</b>: {name_and_price[0][0]}\n'
                f'<b>Цена</b>: {name_and_price[0][1]} <b>RUB</b>\n'
                f'''<b>Последнее обновление</b>: {strftime(
                    "%d.%m.%y, %H:%M MCK",
                    localtime(name_and_price[0][2]))}''',
                parse_mode='HTML',
                reply_markup=kb_delete
        )


async def show_my_status(message: types.Message):
    '''
    '''
    async with transaction() as cur:
        res = cur.execute(f'''
            SELECT * FROM users
            WHERE userid = {int(message.from_user.id)};
        ''').fetchall()

    await message.answer(
        text=f'<b>ID</b>: {res[0][0]}\n'
            f'<b>Username</b>: <i>{res[0][1]}</i>\n'
            f'<b>Статус</b>: <i>{res[0][2]}</i>\n\n'
            f'Сменить свой статус можно написав админу: @forgottenbb',
        parse_mode='HTML'
    )


async def add_premium_user(message: types.Message):
    '''
    '''
    if message.from_user.id != ADMIN_ID:
        return await message.reply('Ты не админ')
    async with transaction() as cur:
        cur.execute(f'''
        UPDATE users
            SET status = 'premium'
            WHERE userid = {int(message.get_args())};''')
    await message.reply(f'{message.get_args()}', reply_markup=kb_cancel_prem)


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(show_my_status,
                                Command(commands=['status']))
    dp.register_message_handler(show_my_status,
                                Text(['status']))
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
    dp.register_message_handler(add_premium_user,
                                Command(commands=['set_premium']))
    dp.register_callback_query_handler(callback_delete, 
                                       text='delete_button_pressed')
    dp.register_callback_query_handler(callback_cancel, 
                                       text='cancel_button_pressed')
    dp.register_callback_query_handler(callback_register,
                                       text='register_button_pressed')
    dp.register_callback_query_handler(callback_cancel_premium,
                                       text='cancel_prem_button_pressed')
