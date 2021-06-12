from apps.bot.tortoise_models import KeyboardButtonsOrdering


async def callback_filter(query, keyboard_name):
    buttons = map(
        str,
        await KeyboardButtonsOrdering.filter(keyboard__code=keyboard_name).values_list('button__code', flat=True)
    )
    return query.data in buttons


def inline_is_digit(query):
    return query.data.isdigit()


def message_is_digit(message):
    return message.text.isdigit()
