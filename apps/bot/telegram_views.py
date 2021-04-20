from aiogram import types

from apps.bot import dispatcher as dp, messages, bot, keyboards
from apps.bot.states import BotForm
from apps.lead.states import CustomerForm, LeadForm
from apps.lead.tortoise_models import Customer
from apps.bot import callback_filters
from apps.bot import keyboards


async def send_main_menu(customer, locale, state=None):
    if state:
        await state.finish()

    if not customer.full_name:
        await CustomerForm.full_name.set()
        return await bot.send_message(
            customer.id,
            await messages.get_message('full_name', locale),
            reply_markup=await keyboards.back_keyboard(locale)
        )

    if not customer.phone_number:
        await CustomerForm.phone_number.set()
        return await bot.send_message(
            customer.id,
            await messages.get_message('phone_number', locale),
            reply_markup=await keyboards.phone_number(locale)
        )

    else:
        await BotForm.main_menu.set()
        await bot.send_message(
            customer.id,
            await messages.get_message('main_menu', locale),
            reply_markup=await keyboards.main_menu(locale)
        )


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, locale):
    user_id = message.from_user.id
    customer = await Customer.filter(id=user_id).first()
    if not customer:
        customer = await Customer.create(id=user_id, username=message.from_user.username)

    await bot.send_message(user_id, await messages.get_message('greeting', locale),
                           reply_markup=keyboards.remove_keyboard)

    if not customer.language:
        await CustomerForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, False))

    await send_main_menu(customer, locale)


@dp.callback_query_handler(callback_filters.main_menu, state=BotForm.main_menu.state)
async def main_menu(query, locale, state):
    user_id = query.from_user.id
    customer = await Customer.get(id=user_id)

    if query.data == 'projects':
        keyboard = await keyboards.project_types(locale)
        message = await messages.get_message('project_type', locale)
        await LeadForm.project_type.set()
        return await bot.edit_message_text(message, user_id, query.message.message_id, reply_markup=keyboard)

    if query.data == 'change_language':
        await CustomerForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, True))

