from core.callback_filters import callback_filter


async def anorhome_menu(query):
    return await callback_filter(query, 'anorhome_menu')


def is_apply(query):
    return 'apply' in query.data