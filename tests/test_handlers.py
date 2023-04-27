from bot.handlers.handlers import help_str, help_command
from unittest.mock import AsyncMock


async def test_help_command():
    message = AsyncMock()
    await help_command(message)
    message.reply.assert_called_with(help_str, parse_mode='HTML')