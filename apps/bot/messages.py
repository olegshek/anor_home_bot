from apps.bot.tortoise_models import Message


async def get_message(code, locale):
    return getattr(await Message.get(code=code), f'text_{locale}')
