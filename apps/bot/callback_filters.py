from apps.bot.tortoise_models import Button
from core.callback_filters import callback_filter
from core.filters import message_keyboard_filter


async def keyboard_back(message):
    back_button = await Button.get(code='back')
    return message.text in [getattr(back_button, f'text_{locale}') for locale in ['ru', 'uz', 'en']]


async def inline_back(query):
    return query.data == 'back'


async def message_is_not_command(message):
    if message.text:
        return not message.text.startswith('/')
    return True


async def message_is_not_back(message):
    back_button = await Button.get(code='back')
    return message.text not in [getattr(back_button, f'text_{locale}') for locale in ['ru', 'uz', 'en']]


async def main_menu(message):
    res = await message_keyboard_filter(message, 'main_menu')
    return res
