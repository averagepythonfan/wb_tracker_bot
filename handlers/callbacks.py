from sqlite3 import IntegrityError
from sqdb import transaction
from aiogram.types import CallbackQuery
from .inlinekb import kb_cancel
from sqlalchemy import text

async def callback_delete(callback: CallbackQuery):
    '''Удаляет выбранный товар из базы данных products
    '''
    txt = callback.message.text
    article = int(txt[9:txt.find('Товар')-1])
    userid = int(callback.from_user.id)
    async with transaction() as cur:
        cur.execute(text(
            f'''DELETE FROM products
            WHERE article = {article} AND userid = {userid};'''))
    await callback.message.delete()
    await callback.message.answer(
        text=f'Товар с артикулом {article} успешно удален',
        reply_markup=kb_cancel
    )
    await callback.answer()


async def callback_cancel(callback: CallbackQuery):
    '''Отменяет удаление'''
    async with transaction() as cur:
        lenght = cur.execute(text(f'''
            SELECT article FROM products
            WHERE userid = {callback.from_user.id};''')).fetchall()
    count = len(lenght)

    async with transaction() as cur:
        status = cur.execute(text(f'''
            SELECT status FROM users
            WHERE userid = {callback.from_user.id}''')).fetchall()
    if count >= 3 and status[0][0] == 'free':
        await callback.answer()
        return await callback.message.answer('Превышен лимит')
    txt = callback.message.text
    article = int(txt[17:txt.find('успешно')-1])
    userid = int(callback.from_user.id)
    async with transaction() as cur:
        cur.execute(text(f'''
            INSERT INTO products
            VALUES ( {article}, {userid});'''))
    await callback.message.delete()
    await callback.message.answer(
        f'Товар с артикулом {article} возвращен в трекер.')
    await callback.answer()


async def callback_register(callback: CallbackQuery):
    '''Регистрирует пользователя в базе данных.
    '''
    try:
        async with transaction() as cur:
            cur.execute(text(
                f'''INSERT INTO users ( userid, username, status)
                        VALUES (
                            {callback.from_user.id},
                            '{callback.from_user.username}',
                            'free'
                        );'''))
        await callback.message.answer('Успешно')
    except IntegrityError:
        await callback.message.answer('Уже зарегистрированы')
    await callback.answer()


async def callback_cancel_premium(callback: CallbackQuery):
    '''Отменяет добавление пользователя в премиум статус.
    '''
    async with transaction() as cur:
        cur.execute(text(f'''
        UPDATE users
            SET status = 'free'
            WHERE userid = {int(callback.message.text)};'''))
    await callback.message.answer('Set "free": Успешно')
    await callback.answer()
