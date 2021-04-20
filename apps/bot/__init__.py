import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from django.conf import settings

app_name = 'bot'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

bot = Bot(token=settings.TELEGRAM_TOKEN)
storage = RedisStorage2(settings.REDIS_HOST, db=5, password=settings.REDIS_PASSWORD)
dispatcher = Dispatcher(bot, storage=storage)
