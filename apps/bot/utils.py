from aiogram.utils.exceptions import TelegramAPIError

from apps.bot import bot


async def try_delete_message(user_id, message_id):
    try:
        await bot.delete_message(user_id, message_id)
    except TelegramAPIError:
        pass
