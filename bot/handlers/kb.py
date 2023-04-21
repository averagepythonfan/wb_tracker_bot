from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

delete_button = InlineKeyboardButton(
    text='Удалить',
    callback_data='delete_button_pressed'
)
kb_delete = InlineKeyboardMarkup(inline_keyboard=[[delete_button]])

cancel_button = InlineKeyboardButton(
    text='Отменить удаление',
    callback_data='cancel_button_pressed'
)
kb_cancel = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])