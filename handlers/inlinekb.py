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
