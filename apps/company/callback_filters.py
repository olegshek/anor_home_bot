from core.callback_filters import callback_filter
from core.filters import message_keyboard_filter, message_button_filter


async def anorhome_menu(message):
    return await message_keyboard_filter(message, 'anorhome_menu')


async def is_apply(message):
    return await message_button_filter(message, 'apply')
