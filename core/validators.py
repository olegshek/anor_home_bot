from asgiref.sync import sync_to_async

from apps.bot.models import Keyboard


@sync_to_async
def keyboard_callback_query(keyboard_name, query):
    buttons = Keyboard.objects.get(name=keyboard_name).buttons.exclude(name='back').values_list('name', flat=True)

    return query.data.split(';')[0] in map(str, buttons)