from aiogram.types import ContentType

from apps.bot import callback_filters as bot_callback_filters, bot, keyboards
from apps.bot import dispatcher as dp
from apps.bot.telegram_views import send_main_menu
from apps.bot.tortoise_models import Button
from apps.lead import callback_filters
from apps.lead.states import CustomerForm
from apps.lead.tortoise_models import Customer


@dp.message_handler(callback_filters.language_choice, state=CustomerForm.language_choice.state)
async def language_choice_processing(message, locale, state):
    user_id = message.from_user.id
    customer = await Customer.get(id=user_id)
    text = message.text
    en_button = await Button.get(code='en')
    ru_button = await Button.get(code='ru')
    language = en_button.code if text == en_button.text_en else ru_button.code if text == ru_button.text_ru else 'uz'
    customer.language = language
    await customer.save()
    await send_main_menu(customer, language, state)


@dp.message_handler(state=CustomerForm.phone_number, content_types=[ContentType.CONTACT])
async def phone_number_save(message, locale, state):
    user_id = message.from_user.id
    customer = await Customer.get(id=user_id)
    contact = message.contact

    if contact.user_id == user_id:
        customer.phone_number = contact.phone_number
        await customer.save()

    await send_main_menu(customer, locale, state)


@dp.message_handler(bot_callback_filters.message_is_not_command, bot_callback_filters.message_is_not_back,
                    state=CustomerForm.full_name.state, content_types=[ContentType.TEXT])
async def full_name_save(message, locale, state):
    user_id = message.from_user.id
    customer = await Customer.get(id=user_id)
    full_name = message.text
    customer.full_name = full_name
    await customer.save()

    await send_main_menu(customer, locale, state)
