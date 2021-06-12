from aiogram import types
from django.conf import settings

from apps.bot import messages
from apps.bot.tortoise_models import Button, KeyboardButtonsOrdering
from apps.lead.tortoise_models import Apartment, Store, Duplex


async def get_back_button_obj():
    return await Button.get(code='back')


async def add_back_inline_button(keyboard, locale):
    back_button_obj = await get_back_button_obj()
    keyboard.add(
        types.InlineKeyboardButton(getattr(back_button_obj, f'text_{locale}'), callback_data=back_button_obj.code)
    )
    return keyboard


async def add_back_reply_button(keyboard, locale):
    back_button_obj = await get_back_button_obj()
    keyboard.add(
        types.KeyboardButton(getattr(back_button_obj, f'text_{locale}'))
    )
    return keyboard


async def language_choice(locale='ru', change=False):
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='language_choice').order_by(
            'ordering'):
        button = await keyboard_button.button
        code = button.code
        buttons.append(types.InlineKeyboardButton(
            button.text_ru if code == 'ru' else button.text_uz if code == 'uz' else button.text_en
        ))

    keyboard.add(*buttons)
    if change:
        await add_back_reply_button(keyboard, locale)
    return keyboard


async def phone_number(locale):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='phone_number').order_by('ordering'):
        button = await keyboard_button.button
        keyboard.add(types.KeyboardButton(
            getattr(button, f'text_{locale}'),
            request_contact=True if button.code == 'phone_number' else None
        ))
    await add_back_reply_button(keyboard, locale)
    return keyboard


async def main_menu(locale):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='main_menu').order_by('ordering'):
        button = await keyboard_button.button
        tg_button = types.InlineKeyboardButton(
            getattr(button, f'text_{locale}'),
            callback_data=button.code,
            url=settings.COMPANY_CHANNEL_URL if button.code == 'subscribe_channel' else None
        )
        buttons.append(tg_button)

    keyboard.add(*buttons)
    return keyboard


async def project_types(locale):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='project_types').order_by('ordering'):
        button = await keyboard_button.button
        tg_button = types.KeyboardButton(getattr(button, f'text_{locale}'))
        buttons.append(tg_button)

    keyboard.add(*buttons)
    await add_back_reply_button(keyboard, locale)
    return keyboard


async def project_choice(project, locale):
    button = await Button.get(code='choose')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        types.InlineKeyboardButton(getattr(button, f'text_{locale}'), callback_data=f'{button.code}:{project.pk}')
    )
    return keyboard


async def cart(locale):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    cart_button = await Button.get(code='cart')
    keyboard.add(types.KeyboardButton(getattr(cart_button, f'text_{locale}')))
    await add_back_reply_button(keyboard, locale)
    return keyboard


async def project_menu(project_type, locale):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_code = 'residential_project_menu' if project_type == 'residential' else 'commercial_project_menu'

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code=keyboard_code).order_by('ordering'):
        button = await keyboard_button.button
        tg_button = types.KeyboardButton(getattr(button, f'text_{locale}'))
        buttons.append(tg_button)

    keyboard.add(*buttons)
    await add_back_reply_button(keyboard, locale)
    return keyboard


async def room_quantity_or_floor_number_choice(project_id, project_type, locale):
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    option_name = 'room_quantity' if project_type == 'residential' else 'floor_number'
    object_model = Apartment if project_type == 'residential' else Store
    filters_params = {'project_id': project_id}

    if project_type == 'residential':
        filters_params['duplex_id__isnull'] = True

    options = list(set(await object_model.filter(**filters_params).values_list(option_name, flat=True)))

    buttons = []
    for option in options:
        buttons.append(types.KeyboardButton(str(option)))

    keyboard.add(*buttons)

    if project_type == 'residential':
        duplexes = await Duplex.filter(project_id=project_id)

        if duplexes:
            duplex_button = await Button.get(code='duplex')
            keyboard.add(types.KeyboardButton(getattr(duplex_button, f'text_{locale}')))

    await add_back_reply_button(keyboard, locale)
    return keyboard


async def project_object_menu(project_object_id, locale, added_objects, projects_quantity, project_number,
                              is_duplex=None, floor_number=None):
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    if is_duplex:
        floor_message = await messages.get_message('floor_number_message', locale)
        floor_switch_buttons = []
        for switch, lookups in zip(['🔽', f'{floor_message} {floor_number}', '🔼'],
                                   ['floor_number__lte', 'ignore', 'floor_number__gte']):
            floor_switch_buttons.append(
                types.InlineKeyboardButton(switch, callback_data=f'{project_object_id};{lookups}')
            )
        keyboard.add(*floor_switch_buttons)

    switch_buttons = []
    for switch, lookups in zip(['◀️', f'{project_number}/{projects_quantity}', '▶️'], ['lte', 'ignore', 'gte']):
        switch_buttons.append(types.InlineKeyboardButton(switch, callback_data=f'{project_object_id};{lookups}'))

    if is_duplex:
        apartment = await Apartment.get(id=project_object_id)
        keyboard_code = 'project_object' if (await apartment.duplex).id not in added_objects else 'added_project_object'
    else:
        keyboard_code = 'project_object' if project_object_id not in added_objects else 'added_project_object'

    keyboard.row(*switch_buttons)

    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code=keyboard_code).order_by('ordering'):
        button = await keyboard_button.button
        code = button.code

        if button.code == 'add_to_cart':
            code = f'{code};{project_object_id}'

        tg_button = types.InlineKeyboardButton(getattr(button, f'text_{locale}'), callback_data=code)
        keyboard.row(tg_button)

    return keyboard


async def cart_inline_menu(transaction_id, locale, transactions_quantity, transaction_number):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    switch_buttons = []
    for switch, lookups in zip(['◀️', f'{transaction_number}/{transactions_quantity}', '▶️'], ['lte', 'ignore', 'gte']):
        switch_buttons.append(types.InlineKeyboardButton(switch, callback_data=f'{transaction_id};{lookups}'))

    keyboard.row(*switch_buttons)

    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='cart_inline_menu').order_by('ordering'):
        button = await keyboard_button.button
        code = button.code

        if button.code == 'remove_from_cart':
            code = f'{code};{transaction_id}'

        tg_button = types.InlineKeyboardButton(getattr(button, f'text_{locale}'), callback_data=code)
        keyboard.row(tg_button)

    return keyboard


async def cart_reply_menu(locale):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='cart_reply_menu').order_by('ordering'):
        button = await keyboard_button.button
        tg_button = types.KeyboardButton(getattr(button, f'text_{locale}'))
        buttons.append(tg_button)

    keyboard.add(*buttons)
    await add_back_reply_button(keyboard, locale)
    return keyboard


async def confirmation(locale):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    confirm_button = await Button.get(code='confirm')
    keyboard.add(
        types.InlineKeyboardButton(getattr(confirm_button, f'text_{locale}'), callback_data=confirm_button.code)
    )

    await add_back_inline_button(keyboard, locale)

    return keyboard


async def anorhome_menu(locale):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='anorhome_menu').order_by('ordering'):
        button = await keyboard_button.button
        tg_button = types.KeyboardButton(getattr(button, f'text_{locale}'))
        buttons.append(tg_button)

    keyboard.add(*buttons)

    await add_back_reply_button(keyboard, locale)
    return keyboard


async def services_or_vacancies(service_or_vacancy, locale, is_last=False):
    button = await Button.get(code='choose')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        types.InlineKeyboardButton(getattr(button, f'text_{locale}'),
                                   callback_data=f'{button.code}:{service_or_vacancy.pk}')
    )
    return keyboard


async def apply(locale):
    button = await Button.get(code='apply')
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton(getattr(button, f'text_{locale}'))
    )
    await add_back_reply_button(keyboard, locale)
    return keyboard


async def back_keyboard(locale):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = await get_back_button_obj()
    keyboard.add(types.KeyboardButton(getattr(button, f'text_{locale}')))
    return keyboard


async def lead_request(apartment_id, locale):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    lead_button = await Button.get(code='lead_request')
    keyboard.add(types.InlineKeyboardButton(
        getattr(lead_button, f'text_{locale}'),
        callback_data=f'lead_request:{apartment_id}')
    )
    await add_back_inline_button(keyboard, locale)

    return keyboard


remove_keyboard = types.ReplyKeyboardRemove()
