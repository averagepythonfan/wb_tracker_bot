__all__ = [
    'commands_for_bot'
]

from aiogram import types


bot_commands = (
    ('help', 'Справка по боту'),
    ('add', '(Артикул товара)'),
    ('status', 'Показывает ваш статус'),
    ('my_products', 'Показывает ваши товары'),
    ('delete', '(Артикул товара)')
)


commands_for_bot = []
for cmd in bot_commands:
    commands_for_bot.append(types.BotCommand(command=cmd[0], description=cmd[1]))