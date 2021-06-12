from apps.bot.tortoise_models import KeyboardButtonsOrdering, Button
from apps.lead.tortoise_models import Customer


async def callback_filter(query, keyboard_name):
    buttons = map(
        str,
        await KeyboardButtonsOrdering.filter(keyboard__code=keyboard_name).values_list('button__code', flat=True)
    )
    return query.data in buttons


async def message_keyboard_filter(message, keyboard_code):
    user = await Customer.filter(id=message.from_user.id).first()
    if not user or not user.language:
        return False

    locale = user.language
    buttons = map(
        str,
        await KeyboardButtonsOrdering.filter(keyboard__code=keyboard_code).values_list(f'button__text_{locale}',
                                                                                       flat=True)
    )
    return message.text in buttons


async def message_button_filter(message, button_code):
    user = await Customer.filter(id=message.from_user.id).first()
    if not user or not user.language:
        return False

    locale = user.language
    button = await Button.get(code=button_code)
    return message.text == getattr(button, f'text_{locale}')
