__all__ = [
    'register_message_handlers'
]


import logging
from aiogram import Router
from aiogram import types
from aiogram.filters.command import Command
from aiogram.filters import Text
from db import async_session_maker, User, Product
from sqlalchemy import delete, select, insert, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from config import ADMIN_ID
from .kb import kb_delete
from .callbacks import callback_cancel, callback_delete


# set logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# help command
help_str = '''Вас привествует бот <b><i>Wildberries-Tracker.</i></b>\n
Чтобы добавить товар в трекер отправьте команду <b>/add</b> <i>(артикул товара)</i> без скобочек и ковычек.\n
При стандартном тарифе у вас в доступе <b>три</b> трекера.\n
Можно в любой момент удалять и добавлять другие товары для трекинга.\n
Проверка цены происходит каждые 1-1,5 часа.\n
Если товар поменяет свою цену, вам придет уведомление от бота.'''


async def help_command(message: types.Message):
    '''help command, that register a new user'''
    async with async_session_maker() as session:
        session: AsyncSession
        query = select(User).where(User.user_id == message.from_user.id)
        user_exist = await session.execute(query)
        # await message.reply(str(user_exist.fetchall()))
        if user_exist.scalars().all():
            await message.reply(help_str, parse_mode='HTML')
            logger.info(f'user {message.from_user.id} is asking for help')
        else:
            new_user = {
                'user_id': message.from_user.id,
                'username': message.from_user.username
            }
            stmt = insert(User).values(**new_user)
            await session.execute(stmt)
            await session.commit()
            await message.reply(help_str, parse_mode='HTML')
            logger.info(f'register a new user {message.from_user.id}')


async def add_product_command(message: types.Message):
    '''Add product to db'''
    try:
        article = int(message.text.split()[1])
    except ValueError:
        return await message.reply('Введите корректный артикул')
    async with async_session_maker() as session:
        session: AsyncSession
        query = select(User.track, func.count(Product.article))\
            .where(User.user_id == message.from_user.id)\
            .join(Product, User.user_id == Product.user_id, isouter=True)\
            .group_by(User.user_id)
        res = await session.execute(query)
        tracks, products = res.fetchall()[0]

        if products < tracks:
            values = {
                'article': article,
                'user_id': message.from_user.id
            }
            query = insert(Product).values(**values)
            await session.execute(query)
            await session.commit()
            await message.reply('Успешно!')
            logger.info(f'user {message.from_user.id} add {article}')
        else:
            await message.reply('Лимит превышен')


async def list_command(message: types.Message):
    '''Return a list of articles'''
    async with async_session_maker() as session:
        session: AsyncSession
        query = select(Product).where(Product.user_id == message.from_user.id)
        res = await session.execute(query)
        for el in res.scalars():
            await message.answer(f'Article {el.article}', reply_markup=kb_delete)
    logger.info(f'user {message.from_user.id} used "/list" command')


async def delete_product_command(message: types.Message):
    '''delete product by article'''
    try:    
        article = int(message.text.split()[1])
        async with async_session_maker() as session:
            session: AsyncSession
            query = query = select(Product).where(Product.user_id == message.from_user.id)
            res = await session.execute(query)
            lst = []
            for el in res.scalars():
                lst.append(el.article)
            if article in lst:
                query = delete(Product).where(Product.article==article)
                await session.execute(query)
                await session.commit()
                await message.reply('Успешно!')
                logger.info(f'user {message.from_user.id} delete article {article}')
            else:
                raise IndexError
    except (ValueError, IndexError):
        return await message.reply('Введите валидный артикул')


async def set_n_trackers_command(message: types.Message):
    '''setting N trackers for user, only for ADMIN'''
    if message.from_user.id == ADMIN_ID:
        args = message.text.split()
        user_id, track = int(args[1]), int(args[2])

        async with async_session_maker() as session:
            session: AsyncSession
            query = update(User).where(User.user_id == user_id).values(track=track)
            await session.execute(query)
            await session.commit()
            await message.reply('Успешно')
            logger.info(f'set {track} for user {user_id}')


async def status_command(message: types.Message):
    '''Return user data'''
    async with async_session_maker() as session:
        session: AsyncSession
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()
        await message.reply(text=f"<b>User ID</b>: <i>{user.user_id}</i>\n"
                            f"<b>User name</b>: <i>{user.username}</i>\n"
                            f"<b>Tracker</b>: {user.track}",
                            parse_mode='HTML')
        logger.info(f'user {message.from_user.id} is asking for status')


def register_message_handlers(router: Router):
    router.message.register(help_command, Command(commands=['help', 'start']))
    router.message.register(status_command, Command(commands=['status']))
    router.message.register(add_product_command, Command(commands=['add']))
    router.message.register(set_n_trackers_command, Command(commands=['set']))
    router.message.register(list_command, Command(commands=['list']))
    router.message.register(delete_product_command, Command(commands=['delete']))

    router.callback_query.register(callback_delete, Text(text=['delete_button_pressed']))
    router.callback_query.register(callback_cancel, Text(text=['cancel_button_pressed']))