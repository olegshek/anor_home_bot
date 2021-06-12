from apps.bot.tortoise_models import Button
from core.filters import message_keyboard_filter, message_button_filter


async def language_choice(message):
    en_text = (await Button.get(code='en')).text_en
    ru_text = (await Button.get(code='ru')).text_ru
    uz_text = (await Button.get(code='uz')).text_uz
    return message.text in [en_text, ru_text, uz_text]


async def project_type(message):
    data =  await message_keyboard_filter(message, 'project_types')
    return data

def choose_button(query):
    data = query.data
    data = data.split(':')

    return 'choose' in data


async def project_menu(message):
    return not await message_button_filter(message, 'cart') and (
            await message_keyboard_filter(message, 'residential_project_menu') or
            await message_keyboard_filter(message, 'commercial_project_menu')
    )


def is_switch(query):
    data = query.data.split(';')
    return len(data) == 2 and data[1] in ['gte', 'lte']


def add_to_cart(query):
    return 'add_to_cart' in query.data


async def cart(message):
    data = await message_button_filter(message, 'cart')
    return data


def cart_inline_menu(query):
    code = query.data.split(';')[0]
    return code == 'remove_from_cart'


async def cart_reply_menu(message):
    return await message_keyboard_filter(message, 'cart_reply_menu')


async def confirm_button(message):
    return await message_button_filter(message, 'confirm')


def is_duplex(query):
    return 'duplex' == query.data


def is_floor_number_switch(query):
    return 'floor_number__gte' in query.data or 'floor_number__lte' in query.data
