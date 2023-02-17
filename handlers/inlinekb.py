__all__ = [
    'kb_delete',
    'kb_cancel'
]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# init inline keyboard
kb_delete = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(
                text='Удалить',
                callback_data='delete_button_pressed')
kb_delete.add(button_1)

kb_cancel = InlineKeyboardMarkup()
button_2 = InlineKeyboardButton(
                text='Отменить удаление',
                callback_data='cancel_button_pressed')
kb_cancel.add(button_2)

kb_register = InlineKeyboardMarkup()
button_3 = InlineKeyboardButton(
                text='Добавить себя в базу данных',
                callback_data='register_button_pressed')
kb_register.add(button_3)

kb_cancel_prem = InlineKeyboardMarkup()
button_4 = InlineKeyboardButton(
                text='Отменить действие',
                callback_data='cancel_prem_button_pressed')
kb_cancel_prem.add(button_4)
