from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert
from db import async_session_maker, Product
from .kb import kb_cancel


async def callback_delete(callback: CallbackQuery):
    '''delete selected product'''

    article = callback.message.text.split()[1]
    async with async_session_maker() as session:
        session: AsyncSession
        query = delete(Product).where(Product.article == int(article))
        await session.execute(query)
        await session.commit()

    await callback.message.reply(f'Успешно, {article}', reply_markup=kb_cancel)
    await callback.answer()


async def callback_cancel(callback: CallbackQuery):
    '''cancel deletion'''
    article = callback.message.text.split()[1]
    async with async_session_maker() as session:
        session: AsyncSession
        values = {
            'article': int(article),
            'user_id': callback.from_user.id
        }
        query = insert(Product).values(**values)
        await session.execute(query)
        await session.commit()
    await callback.message.answer(f'Удаление отменено')
    await callback.answer()