from aiogram import types

from apps.bot import callback_filters
from apps.bot import dispatcher as dp, messages, bot
from apps.bot import keyboards
from apps.bot.callback_filters import keyboard_back, inline_back
from apps.bot.states import BotForm
from apps.bot.tortoise_models import Button
from apps.bot.utils import try_delete_message
from apps.company.states import CompanyForm
from apps.company.tortoise_models import Vacancy, Service
from apps.contact.tortoise_models import ContactText, ContactPhoto, ContactLocation
from apps.lead.states import CustomerForm, LeadForm
from apps.lead.tortoise_models import Customer


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


async def back(user_id, state, locale, message_id=None):
    state_name = await state.get_state()
    customer = await Customer.get(id=user_id)

    try:
        if state_name == CustomerForm.full_name.state:
            await CustomerForm.language_choice.set()
            return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                          reply_markup=await keyboards.language_choice(locale, False))

        if state_name == CustomerForm.phone_number.state:
            await CustomerForm.full_name.set()
            return await bot.send_message(
                customer.id,
                await messages.get_message('full_name', locale),
                reply_markup=await keyboards.back_keyboard(locale)
            )

        if state_name in [
            CompanyForm.menu.state,
            LeadForm.project_type.state,
            CustomerForm.language_choice.state,
            BotForm.contacts.state
        ]:
            if message_id:
                await try_delete_message(user_id, message_id)

            return await send_main_menu(customer, locale, state)

        if state_name == LeadForm.project_choice.state:
            await try_delete_message(user_id, message_id)
            keyboard = await keyboards.project_types(locale)
            message = await messages.get_message('project_type', locale)
            await LeadForm.project_type.set()
            return await bot.send_message(user_id, message, reply_markup=keyboard)

        if state_name in [LeadForm.project_menu.state, LeadForm.cart.state]:
            from apps.lead.telegram_views.project import send_project_choice

            async with state.proxy() as data:
                project_type = data['project_type']

            await try_delete_message(user_id, message_id)
            return await send_project_choice(user_id, message_id, locale, project_type)

        if state_name in [
            LeadForm.room_quantity_or_floor_number_choice.state,
            LeadForm.catalogue.state,
            LeadForm.about_project.state
        ]:
            from apps.lead.telegram_views.project import send_project_menu

            async with state.proxy() as data:
                project_type = data['project_type']
                project_id = data['project_id']

            if message_id:
                await try_delete_message(user_id, message_id)

            return await send_project_menu(user_id, message_id, locale, project_type, project_id)

        if state_name == LeadForm.project_object_choice.state:
            from apps.lead.telegram_views.project import send_room_quantity_or_floor_number

            async with state.proxy() as data:
                project_type = data['project_type']
                project_id = data['project_id']

            return await send_room_quantity_or_floor_number(user_id, message_id, locale, project_id, project_type)

        if state_name == LeadForm.lead_confirmation.state:
            from apps.lead.telegram_views.lead import send_cart_menu
            return await send_cart_menu(user_id, message_id, locale, state)

        if state_name in [CompanyForm.about.state, CompanyForm.vacancies.state, CompanyForm.services.state]:
            message = await messages.get_message('anorhome_menu', locale)
            keyboard = await keyboards.anorhome_menu(locale)

            await CompanyForm.menu.set()
            return await bot.send_message(user_id, message, reply_markup=keyboard)

        if state_name == CompanyForm.vacancy_detail.state:
            vacancies = await Vacancy.all()
            vacancies_len = len(vacancies)

            await bot.send_message(
                user_id,
                messages.get_message('vacancies', locale),
                reply_markup=await keyboards.back_keyboard(locale)
            )

            for vacancy in vacancies:
                is_last = True if vacancies.index(vacancy) == vacancies_len - 1 else False
                photo = await vacancy.photo
                keyboard = await keyboards.services_or_vacancies(vacancy, locale, is_last)

                with open(photo.get_path(), 'rb') as photo_data:
                    await bot.send_photo(
                        user_id,
                        photo_data,
                        caption=getattr(vacancy, f'name_{locale}'),
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )

            return await CompanyForm.vacancies.set()

        if state_name == CompanyForm.cv.state:
            await try_delete_message(user_id, message_id)

            async with state.proxy() as data:
                vacancy_id = data['vacancy_id']

            vacancy = await Vacancy.filter(id=vacancy_id).first()

            if vacancy:
                name = getattr(vacancy, f'name_{locale}')
                description = getattr(vacancy, f'description_{locale}')
                photo = await vacancy.photo
                keyboard = await keyboards.apply(locale)
                message = f'<b>{name}</b>\n\n' \
                          f'{description}'

                await bot.send_message(user_id, '✔️', reply_markup=await keyboards.back_keyboard(locale))

                with open(photo.get_path(), 'rb') as photo_data:
                    await bot.send_photo(
                        user_id,
                        photo_data,
                        caption=message,
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )

                await CompanyForm.vacancy_detail.set()

        if state_name == CompanyForm.service_detail.state:
            services = await Service.all()
            services_len = len(services)

            await bot.send_message(user_id, '✔️', reply_markup=await keyboards.back_keyboard(locale))

            for service in services:
                is_last = True if services.index(service) == services_len - 1 else False
                photo = await service.photo
                keyboard = await keyboards.services_or_vacancies(service, locale, is_last)

                with open(photo.get_path(), 'rb') as photo_data:
                    await bot.send_photo(
                        user_id,
                        photo_data,
                        caption=getattr(service, f'name_{locale}'),
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )

            return await CompanyForm.services.set()

    except Exception:
        await send_main_menu(customer, locale)


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


@dp.message_handler(callback_filters.main_menu, state=BotForm.main_menu.state)
async def main_menu(message, locale, state):
    user_id = message.from_user.id
    code = (await Button.filter(**{f'text_{locale}': message.text}).first()).code

    if code == 'projects':
        keyboard = await keyboards.project_types(locale)
        message = await messages.get_message('project_type', locale)
        await LeadForm.project_type.set()
        return await bot.send_message(user_id, message, reply_markup=keyboard)

    if code == 'change_language':
        await CustomerForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, True))

    if code == 'contacts':
        contact_text = await ContactText.first()
        contact_photos = await ContactPhoto.all()
        contact_location = await ContactLocation.first()

        await bot.send_message(user_id, getattr(contact_text, f'text_{locale}'),
                               reply_markup=await keyboards.back_keyboard(locale))

        for contact_photo in contact_photos:
            photo = await contact_photo.photo
            with open(photo.get_path(), 'rb') as photo_data:
                await bot.send_photo(
                    user_id,
                    photo_data,
                    caption=getattr(photo, f'description_{locale}'),
                    parse_mode='HTML'
                )

        if contact_location:
            location = await contact_location.location
            location_message = await bot.send_location(user_id, location.latitude, location.longitude)
            await bot.send_message(user_id, getattr(location, f'description_{locale}'),
                                   reply_to_message_id=location_message.message_id)

        await BotForm.contacts.set()

    if code == 'anorhome':
        message = await messages.get_message('anorhome_menu', locale)
        keyboard = await keyboards.anorhome_menu(locale)

        await CompanyForm.menu.set()
        await bot.send_message(user_id, message, reply_markup=keyboard)


@dp.message_handler(keyboard_back, state='*')
async def button_back(message, state, locale):
    user_id = message.from_user.id

    await bot.send_message(user_id, '🔙', reply_markup=keyboards.remove_keyboard)
    await back(message.from_user.id, state, locale)


@dp.callback_query_handler(inline_back, state='*')
async def back_inline(query, state, locale):
    await back(query.from_user.id, state, locale, query.message.message_id)
