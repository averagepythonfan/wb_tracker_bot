__all__ = [
    'register_message_handlers'
]

from logger import logger
from config import ADMIN_ID, ADMIN_USERNAME
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from sqdb import transaction
from sqlalchemy import text
from sqlalchemy import exc
from time import localtime, strftime
from .inlinekb import kb_delete
from .callbacks import *


# init exeption
class ZeroValues(BaseException):
    pass


help_str = '''Вас привествует бот Wildberries-Tracker.\n
Чтобы добавить товар в трекер отправьте команду "/add (артикул товара)" без скобочек и ковычек.\n
При стандартном тарифе у вас в доступе три трекера.\n
Можно в любой момент удалять и добавлять другие товары для трекинга.\n
Проверка цены происходит каждые 1-1,5 часа.\n
Если товар поменяет свою цену, вам придет уведомление от бота.'''


async def help_command(message: types.Message):
    '''Отправляет пользователю сообщение с описанием работы бота.'''
    logger.info(f'User {message.from_user.id} is asking for help')
    try:
        async with transaction() as cur:
            cur.execute(text(f'''
                INSERT INTO users ( userid, trackers)
                VALUES ( {message.from_user.id}, 3 );'''))
        logger.info(f'Register new user {message.from_user.id}')
    except exc.IntegrityError:
        logger.info(f'User {message.from_user.id} already exist')
    await message.reply(help_str)


async def echo_command(message: types.Message):
    async with transaction() as cur:
        trackers = cur.execute(text(f'''
            SELECT trackers FROM users
            WHERE userid = {message.from_user.id};''')).fetchall()
    await message.reply(trackers)


async def add_product_command(message: types.Message):
    '''Добавляет продукт в таблицу products.
    Максимальное количество 3 при тарифе "free".
    Не позволяет добавлять продукты не зарегистрированным пользователям.
    Так же не позволяет добавлять не валидные артикулы.
    '''
    logger.debug(f'User {message.from_user.username} add product {message.get_args()}')
    async with transaction() as cur:
        lenght = cur.execute(text(f'''
            SELECT article FROM products
            WHERE userid = {message.from_user.id};''')).fetchall()
    count = len(lenght)

    async with transaction() as cur:
        trackers = cur.execute(text(f'''
            SELECT trackers FROM users
            WHERE userid = {message.from_user.id};''')).fetchall()

    if count < int(trackers[0][0]):
        try:
            async with transaction() as cur:
                cur.execute(text(f'''
                    INSERT INTO products VALUES (
                        {int(message.get_args())},
                        {message.from_user.id});'''))
            await message.reply('Успешно')
        except ValueError:
            await message.reply('Введите валидный артикул')
    else:
        await message.reply('Превышен лимит')


async def delete_product_command(message: types.Message):
    '''Удаляет товар по артикулу.
    Если такого товара нет, сообщает об этом пользователю.
    Если товар успешно удален, также сообщает пользователю.
    '''
    logger.debug(f'User {message.from_user.username} deleted product {message.get_args()}')
    try:
        async with transaction() as cur:
            lenght = cur.execute(text(f'''
                SELECT article FROM products
                WHERE article = {int(message.get_args())}
                AND userid = {message.from_user.id};''')).fetchall()
        count = len(lenght)
        if count == 0:
            raise ZeroValues()

        async with transaction() as cur:
            cur.execute(text(f'''DELETE FROM products
            WHERE article = {int(message.get_args())}
            AND userid = {message.from_user.id};'''))
        await message.reply('Товар успешно удален')
    except ValueError:
        await message.reply('Введите валидный артикул')
    except ZeroValues:
        await message.reply('Нет такого товара')


async def my_products_command(message: types.Message):
    '''Возвращает список отслеживаемых товаров с ценами.
    '''
    logger.debug(f'User {message.from_user.username} asked for products')
    async with transaction() as cur:
        articles = cur.execute(text(f'''
            SELECT article FROM products
            WHERE userid = {message.from_user.id};''')).fetchall()

    for el in articles:
        async with transaction() as cur:
            name_and_price = cur.execute(text(f'''
                SELECT name, price, data FROM tracker
                WHERE article = {el[0]}
                ORDER BY data DESC
                LIMIT 1;''')).fetchall()
        try:
            int(name_and_price[0][1])
        except IndexError:
            await message.answer(
                text=f'Артикул {el[0]} пока не имеет обновлении!\n'
                f'Ближайшее обновление будет в течение часа')
            continue
        await message.answer(
            text=f'<b>Артикул</b>: {str(el[0])}\n'
            f'<b>Товар</b>: {name_and_price[0][0]}\n'
            f'<b>Цена</b>: {name_and_price[0][1]} <b>RUB</b>\n'
            f'''<b>Последнее обновление</b>: {strftime(
                "%d.%m.%y, %H:%M MCK",
                localtime(int(name_and_price[0][2]) + 10800))}''',
            parse_mode='HTML',
            reply_markup=kb_delete)


async def show_my_status(message: types.Message):
    '''Показывает настоящий статус пользователя, его ID и имя.
    '''
    logger.debug(f'User {message.from_user.username} asked for his status')
    async with transaction() as cur:
        res = cur.execute(text(f'''
            SELECT * FROM users
            WHERE userid = {int(message.from_user.id)};
        ''')).fetchall()

    await message.answer(
        text=f'<b>ID</b>: {res[0][0]}\n'
        f'<b>Количество трекеров</b>: <i>{res[0][1]}</i>\n\n'
        f'Сменить свой статус можно написав админу: @{ADMIN_USERNAME}',
        parse_mode='HTML'
    )


async def add_premium_user(message: types.Message):
    '''Меняет статус пользователя на 'premium'.
    Только для админа.
    '''
    logger.debug(f'Admin {message.from_user.username} change {message.get_args()} user status')
    if message.from_user.id != ADMIN_ID:
        return await message.reply('Ты не админ')
    id_and_trackers = message.get_args().split()
    async with transaction() as cur:
        cur.execute(text(f'''
            UPDATE users
            SET trackers = {int(id_and_trackers[1])}
            WHERE userid = {int(id_and_trackers[0])};'''))
    await message.reply(f'{message.get_args()}')


def register_message_handlers(dp: Dispatcher):
    '''Регистрируем обработчики'''
    
    dp.register_message_handler(show_my_status,
                                Command(commands=['status']))
    
    dp.register_message_handler(show_my_status,
                                Text(['status']))
    
    dp.register_message_handler(echo_command,
                                Text(['echo']))
    
    dp.register_message_handler(help_command,
                                Command(commands=['help', 'помощь', 'start']))
    
    dp.register_message_handler(help_command,
                                Text(['help', 'помощь']))
    
    dp.register_message_handler(add_product_command,
                                Command(commands=['add', 'добавь']))
    
    dp.register_message_handler(my_products_command,
                                Command(commands=['my_products', 'продукты']))
    
    dp.register_message_handler(my_products_command,
                                Text(['my_products', 'продукты']))
    
    dp.register_message_handler(delete_product_command,
                                Command(commands=['delete', 'удалить']))
    
    dp.register_message_handler(add_premium_user,
                                Command(commands=['set']))
    
    dp.register_callback_query_handler(callback_delete,
                                       text='delete_button_pressed')
    
    dp.register_callback_query_handler(callback_cancel,
                                       text='cancel_button_pressed')
