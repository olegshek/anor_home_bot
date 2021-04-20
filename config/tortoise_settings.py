from django.conf import settings
from tortoise import Tortoise

from apps.bot import app_name as bot_name
from apps.file import app_name as file_name
from apps.lead import app_name as lead_name


async def init():
    await Tortoise.init(
        db_url=settings.PG_URL,
        modules={
            f'{bot_name}': ['apps.bot.tortoise_models'],
            f'{file_name}': ['apps.file.tortoise_models'],
            f'{lead_name}': ['apps.lead.tortoise_models']
        }
    )


async def start_db_connection():
    await init()
